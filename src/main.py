from conversation import Conversation
from response_generator import generate_responses
from models import ResponseContext
from intents import Intent

conversation = Conversation()

conversation.add_message("partner", "Would you like something to eat?")

context = ResponseContext(conversation=conversation, topics=["applesauce", "soon"], intent=Intent(primary="action", specific="request"))

responses = generate_responses(context=context)

print(responses)