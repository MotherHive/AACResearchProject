import json
from collections.abc import Iterable
from pathlib import Path

from sentence_transformers import SentenceTransformer

PROJECT_FOLDER = Path(__file__).resolve().parents[4]
RESEARCH_FOLDER = PROJECT_FOLDER / "research" / "topic_encoder"


class InferredTopicGenerator:
    def __init__(self):
        self.model = SentenceTransformer(
            str(RESEARCH_FOLDER / "primary_topics_model"),
            device="cuda", 
            local_files_only=True,
        )
        self.model.max_seq_length = 384

        topics_path = RESEARCH_FOLDER / "data" / "finished" / "topics.json"
        with topics_path.open(encoding="utf-8") as file:
            self.topics = json.load(file)

        self.topic_vectors = self.model.encode(
            self.topics,
            normalize_embeddings=True,
            convert_to_tensor=True,
            show_progress_bar=False,
        )

    def generate(
        self,
        turns,
        clue: str,
        excluded_topics: Iterable[str] = (),
    ) -> list[str]:
        prefix = clue.strip().casefold()
        conversation = "\n".join(turn.text for turn in turns)
        excluded = {topic.strip().casefold() for topic in excluded_topics}

        if not prefix or not conversation.strip():
            return []

        matching_indices = [
            index
            for index, topic in enumerate(self.topics)
            if topic.casefold().startswith(prefix)
            and topic.strip().casefold() not in excluded
        ]

        if not matching_indices:
            return []

        conversation_vector = self.model.encode(
            conversation,
            normalize_embeddings=True,
            convert_to_tensor=True,
            show_progress_bar=False,
        )

        matching_vectors = self.topic_vectors[matching_indices]
        scores = matching_vectors @ conversation_vector

        best_indices = scores.topk(
            k=min(6, len(matching_indices))
        ).indices.tolist()

        return [
            self.topics[matching_indices[index]]
            for index in best_indices
        ]
