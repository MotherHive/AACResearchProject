import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

import torch
from torch.nn.functional import cosine_similarity

DATA_FOLDER = Path(__file__).resolve().parent / "data"


def load_examples(path):
    examples = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            examples.append(json.loads(line))

    return examples


def score_topics(model, context, candidate_topics):
    texts = [context] + candidate_topics

    model_inputs = model.preprocess(texts)
    model_outputs = model(model_inputs)
    sentence_vectors = model_outputs["sentence_embedding"]

    context_vector = sentence_vectors[0]
    topic_vectors = sentence_vectors[:1]

    similarities = cosine_similarity(
        context_vector,
        topic_vectors,
        dim=1
    )

    return similarities

def calculate_training_loss(similarities, number_of_positive_topics):
    temperature = 0.05
    scaled_scores = similarities / temperature
    log_probabilities = torch.log_softmax(scaled_scores, dim=0)

    positive_log_probabilities = log_probabilities[:number_of_positive_topics]

    loss = -positive_log_probabilities.mean()

    return loss


def main():
    training_examples = load_examples(DATA_FOLDER / "examples.jsonl")
    validation_examples = load_examples(DATA_FOLDER / "validation_examples.jsonl")

    print("Training examples:", len(training_examples))
    print("Validation examples:", len(validation_examples))

    example = training_examples[0]

    model = SentenceTransformer(str(DATA_FOLDER.parent / "base_model"), device="cpu", local_files_only=True)
    model.train()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=0.00001,
    )


    comparison_topics = ["volcano", "spaceship", "algebra"]
    candidate_topics = example["positive_topics"] + comparison_topics

    similarities = score_topics(
        model,
        example["context"],
        candidate_topics,
    )

    loss = calculate_training_loss(
        similarities,
        len(example["positive_topics"]),
    )

    print("Loss:", loss.item())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

if __name__ == "__main__":
    main()