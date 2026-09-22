import sounddevice as sd
from dotenv import load_dotenv
from inworld_tts import InworldTTS
import asyncio

load_dotenv()

class TTSStream:
    def __init__(self, voice="Dennis", sample_rate=24_000):
        self.voice = voice
        self.sample_rate = sample_rate
        self._tts = InworldTTS()
        self._speaker = sd.RawOutputStream(
            samplerate=self.sample_rate, 
            channels=1, 
            dtype="int16"
        )

    def __enter__(self):
        self._tts = self._tts.__enter__()
        self._speaker = self._speaker.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._speaker.__exit__(exc_type, exc_val, exc_tb)
        self._tts.__exit__(exc_type, exc_val, exc_tb)

    async def speak(self, text: str):
        async for audio_chunk in self._tts.stream(
            text,
            voice=self.voice,
            model="inworld-tts-2",
            delivery_mode="STABLE",
            encoding="PCM",
            sample_rate=self.sample_rate,
            apply_text_normalization="ON",
        ):
            await asyncio.to_thread(self._speaker.write, audio_chunk)