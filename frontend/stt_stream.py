import time
import threading

from moonshine_voice import MicTranscriber


class STTStream:
    def __init__(self, callback=None, language="en", update_interval=0.15):
        self.language = language
        self.update_interval = update_interval

        self._callback = callback
        self._mic = None
        self._thread = None
        self._stop_event = threading.Event()

    def set_callback(self, callback):
        self._callback = callback
        return self

    def _emit(self, event_type, text):
        if self._callback:
            self._callback({
                "type": event_type,
                "text": text,
                "time": time.monotonic(),
            })

    def _on_partial(self, text):
        self._emit("partial", text)

    def _on_final(self, line):
        self._emit("final", line.text)

    def _run(self):
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

                self._stop_event.wait()

        finally:
            self._mic.stop()
            self._mic = None

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()

        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
        )

        self._thread.start()

    def stop(self):
        self._stop_event.set()

        if self._thread:
            self._thread.join()
            self._thread = None