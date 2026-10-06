from collections.abc import Iterable

import spacy

from ...db.models import Turn


TOPIC_LIMIT = 6


class TopicGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def generate(self, turns: Iterable[Turn], clue: str) -> list[str]:
        topics = []

        for turn in reversed(list(turns)):
            topics.extend(self.get_deterministic_topics(turn.text))

        return topics[:TOPIC_LIMIT]

    def get_deterministic_topics(self, sentence: str) -> list[str]:
        doc = self.nlp(sentence)

        topics: list[str] = []

        for chunk in doc.noun_chunks:
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
