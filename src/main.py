from conversation import Conversation
from intents import Intent
from response_generator import generate_responses

@dataclass 
class ResponseContext:
    conversation: Conversation
    topics: list[str]
    intent: Intent | None



conversation = Conversation()

conversation.add_message("user", "Please respond with several responses that include Blue.")

responses = generate_responses(conversation=conversation)