from conversation import Conversation
from response_generator import generate_responses
from models import ResponseContext
from intents import Intent
from tts_stream import TTSStream
from stt_stream import STTStream
import asyncio


async def main():
    conversation = Conversation()

    def handle_stt(event):
        if event["type"] == "final":
            print("\nLIVE AUDIO: ", event["text"])
            conversation.add_message("partner", event["text"])

    stream = STTStream(callback=handle_stt)
    stream.start()

    topics = []
    
    try:
        while True:
            with TTSStream() as tts:
                while True:
                    topic = input("Enter a topic (or none): ")
                    
                    if topic == "":
                        break

                    topics.append(topic)

                print("\nPrimary Intents:")
                primary_intents = Intent.available_primaries()
                for key, description in primary_intents.items():
                    print(f"[{key}] - {description}")

                uinput = input("Type a primary intent key (press Enter for none, or 'q' to quit): ").strip().lower()
                if uinput == "q":
                    break
                
                primary_intent = uinput if uinput != "" else None
                specific_intent = None

                if primary_intent:
                    specific_intents = Intent.available_specifics(primary_intent)
                    print("\nSpecific Intents:")
                    for key, description in specific_intents.items():
                        print(f"[{key}] - {description}")
                    
                    sinput = input("Select a specific intent (press Enter for none): ").strip().lower()
                    specific_intent = sinput if sinput != "" else None
                    
                print(f"User selected Topics: {topics} | Intent: {primary_intent} - {specific_intent}\n")

                context = ResponseContext(
                    conversation=conversation, 
                    topics=topics, 
                    intent=Intent(primary=primary_intent, specific=specific_intent)
                )
                
                responses = generate_responses(context=context).responses

                for i in range(len(responses)):
                    print(f"{i+1}. {responses[i]}\n")

                selection = int(input("Select a response: "))
                conversation.add_message("user", responses[selection-1])
                await tts.speak(responses[selection-1])
                
                topics.clear()
                
    finally:
        stream.stop()

if __name__ == "__main__":
    asyncio.run(main())