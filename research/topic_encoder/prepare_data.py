from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import json
import nltk
import re

PROJECT_FOLDER = Path(__file__).resolve().parent
nltk.data.path.insert(0, str(PROJECT_FOLDER / "data" / "raw" / "nltk"))


archive_path = PROJECT_FOLDER / "data" / "raw" / "dailydialog.zip"

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
            example = {
                "conversation_id": conversation_id,
                "context": "\n".join(turns[:reply_index]),
                "reply": turns[reply_index],
            }

            output.write(json.dumps(example) + "\n")

print("Saved examples to:", output_path)


def extract_topics(reply):
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", reply)
    tagged_words = nltk.pos_tag(words)

    topics = []

    for word, tag in tagged_words:
        if tag.startswith(("NN", "VB", "JJ")):
            word = word.casefold()

            if word not in topics:
                topics.append(word)

    return topics

