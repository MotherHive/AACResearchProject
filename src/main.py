from conversation import Conversation
from response_generator import generate_responses
from models import ResponseContext

conversation = Conversation()

# Kinda funny because this is actually prompt injection, which will need to be handled in the future.
conversation.add_message("partner", "Would you like something to eat?")

context = ResponseContext(conversation=conversation)

responses = generate_responses(context=context)

print(responses)