
const CONVERSATIONS_ENDPOINT = "http://localhost:8000/api/v1/conversations";

type Conversation = {
    id: string;
    created_at: string;
};

export async function createConversation(): Promise<Conversation> {
    const response = await fetch(CONVERSATIONS_ENDPOINT, { method: "POST" });

    return response.json();
}

export async function createTurn(conversationId: string, speaker: "user" | "partner", text: string): Promise<void> {
    const url = `${CONVERSATIONS_ENDPOINT}/${conversationId}/turns`

    await fetch(
        url,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                speaker,
                text,
            }),
        },
    );
}