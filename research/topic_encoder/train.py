import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

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

    model = SentenceTransformer(str(DATA_FOLDER.parent / "base_model"), device="cpu", local_files_only=True)
    model.train()


    texts = [example["context"]] + example["positive_topics"]

    inputs = model.preprocess(texts)
    outputs = model(inputs)
    vectors = outputs["sentence_embedding"]

    print("Vector shape:", vectors.shape)
    print("Tracks gradients:", vectors.requires_grad)


if __name__ == "__main__":
    main()