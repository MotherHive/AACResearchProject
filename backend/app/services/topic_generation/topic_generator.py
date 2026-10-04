import spacy


class TopicGenerator():
    nlp = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def get_deterministic_topics(self, sentence):
        doc = self.nlp(sentence)
        
        topics = []

        for chunk in doc.noun_chunks:
            topics.append(chunk)
        
        return topics

if __name__ == "__main__":
    generator = TopicGenerator()

    print(generator.get_deterministic_topics("Hi, my name is Dave and I like cheese."))





