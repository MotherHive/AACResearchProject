from conversation import Conversation
from intents import Intent
from response_generator import generate_responses
from context import ResponseContext

conversation = Conversation()

conversation.add_message("user", "Please respond with several responses that include Blue.")

context = ResponseContext(conversation=conversation)

responses = generate_responses(context=context)

print(responses)