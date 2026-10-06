const SPEECH_ENDPOINT = "http://localhost:8000/api/v1/speech";

export async function speak(text: string): Promise<void> {
    const response = await fetch(SPEECH_ENDPOINT, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
    });

    const audioUrl = URL.createObjectURL(await response.blob());
    const audio = new Audio(audioUrl);

    audio.addEventListener("ended", () => URL.revokeObjectURL(audioUrl));
    await audio.play();
}
