import time
import json

from moonshine_voice import MicTranscriber


class STTStream:
    def __init__(self, language="en", update_interval=0.15):
        self.language = language
        self.update_interval = update_interval

        self._callback = None
        self._mic = None
        self._stop_event = threading.Event()

    def set_callback(self, callback):
        self._callback = callback

    def _emit(self, event_type, text):
        event = {
            "type": event_type,
            "text": text,
            "time": time.monotonic(),
        }

        if self._callback:
            self._callback(event)

    def _on_partial(self, text):
        self._emit("partial", text)

    def _on_final(self, line):
        self._emit("final", line.text)

    def start(self):
        self._stop_event.clear()

        self._mic = (
            MicTranscriber()
            .language(self.language)
            .update_interval(self.update_interval)
            .on_text(self._on_partial)
            .on_line(self._on_final)
        )

        self._mic.load()

        try:
            with self._mic:
                self._mic.start()

                while not self._stop_event.wait(0.05):
                    pass

        finally:
            self._mic.stop()
            self._mic = None

    def stop(self):
        self._stop_event.set()
