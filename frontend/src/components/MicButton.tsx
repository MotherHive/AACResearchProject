import { useRef, useState } from "react";
import { recordPCM } from "record-pcm";
import type { StreamingTranscriber } from "assemblyai/streaming";
import { connectAssemblyAI } from "../services/assemblyaiStreaming";

type Status = "idle" | "connecting" | "recording" | "stopping";

type MicButtonProps = {
    onFinalTranscript: (text: string) => void;
}

export default function MicButton(props: MicButtonProps) {
    const [status, setStatus] = useState<Status>("idle");
    const [transcript, setTranscript] = useState("");
    const [error, setError] = useState<string | null>(null);

    const SAMPLE_RATE = 16000

    const stopRecorderRef = useRef<(() => void) | null>(null);

    const transcriberRef =
        useRef<StreamingTranscriber | null>(null);

    async function startRecording() {
        if (status !== "idle") {
            return;
        }

        setStatus("connecting");
        setError(null);
        setTranscript("");

        try {
            const connectionPromise = connectAssemblyAI({
                onTurn: (turn) => {
                    if (turn.end_of_turn) { // This checks if it's a final answer, might turn this into partial later
                        setTranscript(turn.transcript); 
                        props.onFinalTranscript(turn.transcript)
                    } 
                },

                onError: (error) => {
                    console.error("Error:", error);
                    setError(error.message);
                },
            });

            stopRecorderRef.current = recordPCM({
                sampleRate: SAMPLE_RATE,

                onData: ({ pcm }) => {
                    const transcriber = transcriberRef.current;

                    if (transcriber) {
                        transcriber.sendAudio(pcm.buffer);
                    } 
                },

                onError: (error) => { setError(error.message)},
            });

            const transcriber = await connectionPromise;

            transcriberRef.current = transcriber;
            setStatus("recording");
            
        } catch (error) {
            stopRecorderRef.current?.();
            stopRecorderRef.current = null;

            const message =
            error instanceof Error
                ? error.message
                : "Could not start transcription";

            setError(message);
            setStatus("idle");
        }
    }

    async function stopRecording() {
        setStatus("stopping");

        if (stopRecorderRef.current) {stopRecorderRef.current();}
        stopRecorderRef.current = null;

        const transcriber = transcriberRef.current;
        transcriberRef.current = null;

        try {
            if (transcriber) {await transcriber.close()}
        } catch (error) {
            console.error("Could not close AssemblyAI:", error);
        } finally {
            setStatus("idle");
        }
    }

    function toggleRecording() {
        if (status === "idle") {
            startRecording();
        } else if (status === "recording") {
            stopRecording();
        }
    }

    const buttonText = {
        idle: "Enable Microphone",
        connecting: "Connecting...",
        recording: "Disable Microphone",
        stopping: "Stopping...",
    }[status];

    return (
        <div>
        <button
            type="button"
            onClick={toggleRecording}
            disabled={
                status === "connecting" || status === "stopping"
            }
        >
            {buttonText}
        </button>

        {transcript && <p>{transcript}</p>}
        {error && <p>{error}</p>}
        </div>
    );
}