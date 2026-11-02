from pathlib import Path
from zipfile import ZipFile
from io import BytesIO
import json
import re


PROJECT_FOLDER = Path(__file__).resolve().parent

archive_path = PROJECT_FOLDER / "data" / "raw" / "dailydialog.zip"
output_path = PROJECT_FOLDER / "data" / "examples.jsonl"


def tokenize_reply(reply):
    reply = reply.replace("’", "'")

    # Join spaced contractions from the dataset.
    reply = re.sub(
        r"\b([A-Za-z]+)\s*'\s*(t|s|m|d|re|ve|ll)\b",
        r"\1'\2",
        reply,
        flags=re.IGNORECASE,
    )

    abbreviation_pattern = r"(?:[A-Za-z]\.)+[A-Za-z]\.?"
    number_pattern = r"[0-9]+(?:[.,:/][0-9]+)+"
    word_pattern = r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*"

    pattern = "|".join([
        abbreviation_pattern,
        number_pattern,
        word_pattern,
    ])

    words = []

    for token in re.findall(pattern, reply):
        if re.fullmatch(abbreviation_pattern, token):
            token = token.replace(".", "")

        words.append(token)

    return words

def extract_topics(reply):
    topics = []

    for word in tokenize_reply(reply):
        topic = word.casefold()

        if topic not in topics:
            topics.append(topic)

    return topics
    

def load_conversations(split):
    with ZipFile(archive_path) as archive:
        split_zip = archive.read(f"EMNLP_dataset/{split}.zip")

    with ZipFile(BytesIO(split_zip)) as archive:
        filename = f"{split}/dialogues_{split}.txt"
        contents = archive.read(filename).decode("utf-8")

    return contents.splitlines()


def save_examples(conversations, output_path):
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
                    "id": f"{conversation_id}_{reply_index}",
                    "conversation_id": conversation_id,
                    "turn_index": reply_index,
                    "context": "\n".join(turns[:reply_index]),
                    "reply": reply,
                    "candidates": topics,
                }
                output.write(json.dumps(example) + "\n")

    print("Saved examples to:", output_path)




def save_topics():
    topics = set()

    with output_path.open("r", encoding="utf-8") as file:
        for line in file:
            example = json.loads(line)
            topics.update(example["candidates"])

    topics_path = PROJECT_FOLDER / "data" / "topics.json"

    with topics_path.open("w", encoding="utf-8") as file:
        json.dump(sorted(topics), file, ensure_ascii=False, indent=2)

    print("Saved unique topics:", len(topics))


def main():
    conversations = load_conversations("train")
    validation_conversations = load_conversations("validation")

    validation_path = PROJECT_FOLDER / "data" / "validation_examples.jsonl"

    save_examples(conversations, output_path)
    save_examples(validation_conversations, validation_path)
    save_topics()



if __name__ == "__main__":
    main()