import json
from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent / "data"


def load_examples(path):
    examples = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            examples.append(json.loads(line))

    return examples


def main():
    training_examples = load_examples(DATA_FOLDER / "examples.jsonl")
    validation_examples = load_examples(DATA_FOLDER / "validation_examples.jsonl")

    print("Training examples:", len(training_examples))
    print("Validation examples:", len(validation_examples))

    example = training_examples[0]
    print("Context:", example["context"])
    print("Positive topics:", example["positive_topics"])


if __name__ == "__main__":
    main()