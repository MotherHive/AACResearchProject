import spacy


class TopicGenerator():
    nlp = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def get_deterministic_topics(self, sentence):
        doc = self.nlp(sentence)
        
        topics = []

        for chunk in doc.noun_chunks:
            if chunk.root.pos_ == "PRON":
                continue

            cleaned_chunk = self.remove_filler(chunk)

            topics.append(cleaned_chunk)
        
        return topics

    def remove_filler(self, chunk):
        cleaned_tokens = []
        
        for token in chunk:
            if token.pos_ in ["NOUN", "PROPN"]:
                cleaned_tokens.append(token.text)

        return " ".join(cleaned_tokens).strip()

if __name__ == "__main__":
    generator = TopicGenerator()

    print(generator.get_deterministic_topics("Call me Ishmael. Some years ago--never mind how long precisely--having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. "))





