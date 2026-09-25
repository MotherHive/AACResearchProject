from collections.abc import AsyncIterator

from dotenv import load_dotenv
from inworld_tts import InworldTTS

load_dotenv()

VOICE = "Dennis"
SAMPLE_RATE = 24_000


async def stream_speech(text: str) -> AsyncIterator[bytes]:
    with InworldTTS() as tts:
        async for audio_chunk in tts.stream(
            text,
            voice=VOICE,
            model="inworld-tts-2",
            delivery_mode="STABLE",
            encoding="PCM",
            sample_rate=SAMPLE_RATE,
            apply_text_normalization="ON",
        ):
            yield audio_chunk