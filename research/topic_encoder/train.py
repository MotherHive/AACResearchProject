import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

import random

import torch
from torch.nn.functional import cosine_similarity

PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FOLDER = PROJECT_FOLDER / "data" / "finished"


def load_examples(path):
    examples = []

    with path.open(encoding="utf-8") as file:
        for line in file:
            examples.append(json.loads(line))

    return examples


def encode_texts(model, texts):
    model_inputs = model.preprocess(texts, max_length=384)

    for name, value in model_inputs.items():
        if isinstance(value, torch.Tensor):
            model_inputs[name] = value.to(model.device)

    model_outputs = model(model_inputs)

    return model_outputs["sentence_embedding"]


def score_topics(model, context, candidate_topics):
    context_vectors = encode_texts(model, [context])
    topic_vectors = encode_texts(model, candidate_topics)

    context_vector = context_vectors[0]

    similarities = cosine_similarity(
        context_vector,
        topic_vectors,
        dim=1,
    )

    return similarities

def calculate_training_loss(similarities, number_of_positive_topics):
    temperature = 0.05
    scaled_scores = similarities / temperature
    log_probabilities = torch.log_softmax(scaled_scores, dim=0)

    positive_log_probabilities = log_probabilities[:number_of_positive_topics]

    loss = -positive_log_probabilities.mean()

    return loss


def train_on_example(model, optimizer, example, comparison_topics):
    optimizer.zero_grad()

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

    loss.backward()
    optimizer.step()

    return loss.item()


def choose_comparison_topics(all_topics, positive_topics, count=10):
    available_topics = []

    for topic in all_topics:
        if topic not in positive_topics:
            available_topics.append(topic)

    number_to_choose = min(count, len(available_topics))

    return random.sample(available_topics, number_to_choose)


def train_one_epoch(model, optimizer, examples, all_topics):
    model.train()
    total_loss = 0

    

    for step, example in enumerate(examples, start=1):
        comparison_topics = choose_comparison_topics(
            all_topics,
            example["positive_topics"],
        )

        loss = train_on_example(
            model,
            optimizer,
            example,
            comparison_topics,
        )

        total_loss += loss
        if step % 100 == 0: print("Trained:", step, "/", len(examples))

    average_loss = total_loss / len(examples)

    return average_loss

def measure_example_loss(model, example, comparison_topics):
    model.eval()

    with torch.no_grad():
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

    return loss.item()


def prepare_validation_cases(examples, all_topics):
    validation_cases = []

    for example in examples:
        comparison_topics = choose_comparison_topics(
            all_topics,
            example["positive_topics"],
        )

        validation_cases.append((example, comparison_topics))

    return validation_cases


def measure_validation_loss(model, validation_cases):
    total_loss = 0

    for example, comparison_topics in validation_cases:
        loss = measure_example_loss(
            model,
            example,
            comparison_topics,
        )

        total_loss += loss

    return total_loss / len(validation_cases)

def main():
    training_examples = load_examples(DATA_FOLDER / "examples.jsonl")
    validation_examples = load_examples(DATA_FOLDER / "validation_examples.jsonl")

    print("Training examples:", len(training_examples))
    print("Validation examples:", len(validation_examples))

    model = SentenceTransformer(str(PROJECT_FOLDER / "base_model"), device="cuda", local_files_only=True)
    model.float()
    model.train()
    
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=0.00001,
    )
    
    with (DATA_FOLDER / "topics.json").open(encoding="utf-8") as file:
        all_topics = json.load(file)

    random.seed(42) 

    practice_examples = training_examples.copy()
    random.shuffle(practice_examples)
    number_of_epochs = 1

    validation_cases = prepare_validation_cases(
        random.sample(validation_examples, 200),
        all_topics,
    )

    loss_before_training = measure_validation_loss(
        model,
        validation_cases,
    )


    print("Validation before training:", round(loss_before_training, 4))

    for epoch in range(1, number_of_epochs + 1):
        average_loss = train_one_epoch(
            model,
            optimizer,
            practice_examples,
            all_topics,
        )

        print("Epoch:", epoch, "Average loss:", round(average_loss, 4))

    loss_after_training = measure_validation_loss(
        model,
        validation_cases,
    )

    print("Validation after training:", round(loss_after_training, 4))

    output_folder = PROJECT_FOLDER / "primary_topics_model"

    model.save(
        str(output_folder),
        create_model_card=False,
    )

    print("Saved model to:", output_folder)

if __name__ == "__main__":
    main()