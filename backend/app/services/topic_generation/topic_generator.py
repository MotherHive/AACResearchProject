from collections.abc import Iterable

import spacy
from spacy.util import filter_spans

from ...db.models import Turn


TOPIC_LIMIT = 6
TOPIC_ENTITY_LABELS = {
    "PERSON", "NORP", "FAC", "ORG", "GPE", "LOC",
    "PRODUCT", "EVENT", "WORK_OF_ART", "LANGUAGE",
}


class TopicGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")

    def generate(self, turns: Iterable[Turn], clue: str) -> list[str]:
        topics = []
        prefix = clue.strip().casefold()

        for turn in reversed(list(turns)):
            topics.extend(self.get_deterministic_topics(turn.text))

        unique_topics = []
        seen = set()

        for topic in topics:
            normalized_topic = topic.strip().casefold()

            if not normalized_topic.startswith(prefix):
                continue

            if normalized_topic in seen:
                continue

            seen.add(normalized_topic)
            unique_topics.append(topic)

        return unique_topics[:TOPIC_LIMIT]

    def get_deterministic_topics(self, sentence: str) -> list[str]:
        doc = self.nlp(sentence)

        entities = [entity for entity in doc.ents if entity.label_ in TOPIC_ENTITY_LABELS]
        # Keep full proper-name chunks when NER recognizes only part of the name.
        names = [
            chunk for chunk in doc.noun_chunks
            if all(token.pos_ == "PROPN" for token in chunk)
        ]
        entities = filter_spans(entities + names)
        topics = [entity.text for entity in entities]

        for chunk in doc.noun_chunks:
            if any(chunk.start < entity.end and entity.start < chunk.end for entity in entities):
                continue

            if chunk.root.pos_ == "PRON":
                continue

            cleaned_chunk = self.remove_filler(chunk)

            if cleaned_chunk:
                topics.append(cleaned_chunk)

        return topics

    def remove_filler(self, chunk) -> str:
        cleaned_tokens = []

        for token in chunk:
            if token.pos_ in ["NOUN", "PROPN"]:
                cleaned_tokens.append(token.text)

        return " ".join(cleaned_tokens).strip()
