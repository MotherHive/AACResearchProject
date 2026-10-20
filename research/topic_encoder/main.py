import json
from pathlib import Path


from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity

topics_path = Path(__file__).resolve().parent / "data" / "topics.json"

with topics_path.open(encoding="utf-8") as file:
    topics = json.load(file)

model = SentenceTransformer(
    "./base_model",
    device="cpu",
    local_files_only=True,
)

def filter_topics(topics, prefix):
    matches = []
    for topic in topics:
        if topic.casefold().startswith(prefix.casefold()):
            matches.append(topic)

    return matches

def rank_topics(model, conversation, topics):
    conversation_vector = model.encode(conversation, convert_to_tensor=True)
    topic_vectors = model.encode(matching_topics, convert_to_tensor=True)

    results = []

    for topic, topic_vector in zip(matching_topics, topic_vectors):
        score = cosine_similarity(conversation_vector, topic_vector, dim=0)
        results.append((score.item(), topic))

    results.sort(reverse=True)
    return results


conversation = "I need someone to fix my car."
prefix = "a"

matching_topics = filter_topics(topics=topics, prefix=prefix)

if matching_topics:
    results = rank_topics(model, conversation, matching_topics)

    for score, topic in results[:6]:
        print(topic, round(score, 3))
else:
    print("No matching topics.")