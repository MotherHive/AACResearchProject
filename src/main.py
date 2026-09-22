from conversation import Conversation
from response_generator import generate_responses
from models import ResponseContext
from intents import Intent
from tts_stream import TTSStream
import asyncio


async def main():
    with TTSStream() as tts:
        conversation = Conversation()

        conversation.add_message("partner", "Would you like something to eat?")

        context = ResponseContext(conversation=conversation, topics=["applesauce", "soon"], intent=Intent(primary="action", specific="request"))

        responses = generate_responses(context=context).responses

        for i in range(len(responses)):
            print(f"{i+1}. {responses[i]}\n")

        selection = int(input("Select a response:"))

        await tts.speak(responses[selection-1])




asyncio.run(main())

