from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import json
import re

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer


PROJECT_FOLDER = Path(__file__).resolve().parent
nltk.data.path.insert(0, str(PROJECT_FOLDER / "data" / "raw" / "nltk"))


archive_path = PROJECT_FOLDER / "data" / "raw" / "dailydialog.zip"


def tokenize_reply(reply):
    reply = reply.replace("’", "'")

    # Join spaced contractions
    reply = re.sub(
        r"\b([A-Za-z]+)\s*'\s*(t|s|m|d|re|ve|ll)\b",
        r"\1'\2",
        reply,
        flags=re.IGNORECASE,
    )

    words = []

    for token in TreebankWordTokenizer().tokenize(reply):
        if re.fullmatch(r"(?:[A-Z]\.)+[A-Z]\.?", token):
            # Preserve abbreviations
            words.append(token.replace(".", ""))
        else:
            # Separate words joined by periods
            words.extend(token.replace(".", " . ").split())

    return words


def extract_topics(reply):
    lemmatizer = WordNetLemmatizer()
    word_types = {"NN": "n", "VB": "v", "JJ": "a"}
    IGNORED_TOPICS = {"be", "do", "have"}
    topics = []

    for word, tag in nltk.pos_tag(tokenize_reply(reply)):
        if not re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", word):
            continue

        if len(word) < 2 or word.casefold() == "n't":
            continue

        word_type = word_types.get(tag[:2])

        if word_type is None:
            continue

        if tag in {"NNP", "NNPS"}:
            topic = word
        else:
            topic = lemmatizer.lemmatize(word.casefold(), pos=word_type)

        if topic.casefold() in IGNORED_TOPICS:
            continue

        if topic not in topics:
            topics.append(topic)

    return topics



with ZipFile(archive_path) as archive:
    training_zip = archive.read("EMNLP_dataset/train.zip")

with ZipFile(BytesIO(training_zip)) as archive:
    contents = archive.read("train/dialogues_train.txt").decode("utf-8")

conversations = contents.splitlines()
output_path = PROJECT_FOLDER / "data" / "examples.jsonl"

with output_path.open("w", encoding="utf-8") as output:
    for conversation_id, conversation in enumerate(conversations):
        turns = []

        for text in conversation.split("__eou__"):
            text = text.strip()

            if text:
                turns.append(text)

        for reply_index in range(1, len(turns)):
            reply = turns[reply_index]
            topics = extract_topics(reply)

            if not topics:
                continue

            example = {
                "conversation_id": conversation_id,
                "context": "\n".join(turns[:reply_index]),
                "reply": reply,
                "positive_topics": topics,
            }

            output.write(json.dumps(example) + "\n")

print("Saved examples to:", output_path)



topics = set()

with output_path.open("r", encoding="utf-8") as file:
    for line in file:
        example = json.loads(line)
        topics.update(example["positive_topics"])

topics_path = PROJECT_FOLDER / "data" / "topics.json"

with topics_path.open("w", encoding="utf-8") as file:
    json.dump(sorted(topics), file, ensure_ascii=False, indent=2)

print("Saved unique topics:", len(topics))