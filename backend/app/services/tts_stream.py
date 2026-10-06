from collections.abc import AsyncIterator
from io import BytesIO
import wave

from dotenv import load_dotenv
from inworld_tts import InworldTTS

load_dotenv()

VOICE = "Dennis"
SAMPLE_RATE = 24_000


async def stream_speech(text: str) -> AsyncIterator[bytes]:
    audio = bytearray()

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
            audio.extend(audio_chunk)

    wav = BytesIO()

    with wave.open(wav, "wb") as audio_file:
        audio_file.setnchannels(1)
        audio_file.setsampwidth(2)
        audio_file.setframerate(SAMPLE_RATE)
        audio_file.writeframes(audio)

    yield wav.getvalue()
