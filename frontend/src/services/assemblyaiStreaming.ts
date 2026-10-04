import {StreamingTranscriber, type TurnEvent} from "assemblyai/streaming";

type SessionResponse = {
    token: string;
    expires_in_seconds: number;
    max_session_duration_seconds: number;
};

type StreamingCallbacks = {
    onTurn: (turn: TurnEvent) => void;
    onError: (error: Error) => void;
};

const STT_ENDPOINT = "http://localhost:8000/api/v1/stt/sessions" // Gonna need to change this later.

export async function connectAssemblyAI(callbacks: StreamingCallbacks,): Promise<StreamingTranscriber> {
    const response = await fetch(STT_ENDPOINT, { method: "POST" },);

    const session: SessionResponse = await response.json();

    const transcriber = new StreamingTranscriber({
        token: session.token,
        sampleRate: 16000,
        encoding: "pcm_s16le",
        speechModel: "universal-3-6-pro",
        mode: "balanced",
        includePartialTurns: true,
    });

    transcriber.on("turn", callbacks.onTurn);
    transcriber.on("error", callbacks.onError);

    await transcriber.connect();

    return transcriber;
}
