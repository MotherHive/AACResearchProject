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


def extract_topics(reply):
    '''
        Takes a string and extracts the words into an array of WordNet useable items.
    '''
    lemmatizer = WordNetLemmatizer()
    word_types = {"NN": "n", "VB": "v", "JJ": "a"}

    
    reply = reply.replace("’", "'")
    words = TreebankWordTokenizer().tokenize(reply)
    tagged_words = nltk.pos_tag(words)
    topics = []

    for word, tag in tagged_words:
        if word.startswith("'") or word.casefold() == "n't":
            continue
        
        word_type = word_types.get(tag[:2])

        if word_type is None:
            continue

        if tag in {"NNP", "NNPS"}: # If a proper noun then keep it capitalized to be recognized correctly by the lemmatizer
            topic = word
        else:
            topic = lemmatizer.lemmatize(word.casefold(), pos=word_type)

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