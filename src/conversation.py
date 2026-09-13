from dataclasses import dataclass

@dataclass
class ConversationTurn:
    speaker: str
    text: str

class Conversation:
    def __init__(self):
        self.history: list[ConversationTurn] = []

    def add_message(self, speaker, text):
        turn = ConversationTurn(speaker=speaker, text=text)

        self.history.append(turn)

    def get_last_message(self):
        return self.history[-1]

    def get_history(self):
        return self.history

    def get_history_str(self) -> str:
        text = "\n".join(
            f'{turn.speaker}: {turn.text}'
            for turn in self.history)

        return text
