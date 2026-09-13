from conversation import Conversation
from response_generator import generate_responses
from models import ResponseContext

conversation = Conversation()

conversation.add_message("partner", "Would you like something to eat?")

context = ResponseContext(conversation=conversation)

responses = generate_responses(context=context)

print(responses)