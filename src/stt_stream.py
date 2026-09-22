import time
import json

from moonshine_voice import MicTranscriber



def emit_final(line):
    event = {
        "type": "final",
        "text": line.text,
        "time": time.monotonic()
    }

    print(f"Emitting: ", json.dumps(event))
    return event

def emit_partial(text):
    event = {
        "type": "partial",
        "text": text,
        "time": time.monotonic()
    }

    print(f"Emitting: ", json.dumps(event))
    return event



def main():
    mic = (
            MicTranscriber()
            .language("en")
            .update_interval(0.15)
            .on_text(emit_partial)
            .on_line(emit_final)
        )

    print("Loading model...")
    mic.load()

    print("Listening...")

    with mic:
        mic.start()

        try:
            while True:
                time.sleep(0.05)

        except KeyboardInterrupt:
            print("\nStopping...")

        finally:
            mic.stop()

if __name__ == "__main__":
    main()
