from sentence_transformers import SentenceTransformer
from torch.nn.functional import cosine_similarity

model = SentenceTransformer(
    "./base_model",
    device="cpu",
    local_files_only=True,
)

conversation = "I need someone to fix my car."
topics = ["apple", "mechanic", "engine", "holiday"]

conversation_vector = model.encode(conversation, convert_to_tensor=True)

topic_vectors = model.encode(topics, convert_to_tensor=True)

results = []

for topic, topic_vector in zip(topics, topic_vectors):
    score = cosine_similarity(conversation_vector, topic_vector, dim=0)
    results.append((score.item(), topic))

results.sort(reverse=True)

for score, topic in results:
    print(topic, round(score, 3))