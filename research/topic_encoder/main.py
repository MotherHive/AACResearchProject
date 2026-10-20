from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity

model = SentenceTransformer(
    "./base_model",
    device="cpu",
    local_files_only=True,
)

conversation = "I need someone to fix my car."
topics = ["apple", "ample", "arrow", "mechanic", "engine", "holiday"]
prefix = "a"

def filter_topics(topics, prefix):
    matches = []
    for topic in topics:
        if topic.startswith(prefix):
            matches.append(topic)

    return matches

matching_topics = filter_topics(topics=topics, prefix=prefix)

conversation_vector = model.encode(conversation, convert_to_tensor=True)

topic_vectors = model.encode(matching_topics, convert_to_tensor=True)

results = []

for topic, topic_vector in zip(matching_topics, topic_vectors):
    score = cosine_similarity(conversation_vector, topic_vector, dim=0)
    results.append((score.item(), topic))

results.sort(reverse=True)

for score, topic in results:
    print(topic, round(score, 3))