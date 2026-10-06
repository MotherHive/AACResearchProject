
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

type TopicOptions = {
    topics: string[];
};

export async function generateTopics(conversationId: string, clue: string): Promise<string[]> {
    const response = await fetch(
        `${CONVERSATIONS_ENDPOINT}/${conversationId}/topics`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({clue}),
        }
    );

    const result: TopicOptions = await response.json();
    return result.topics;
}

type ResponseOptions = {
    responses: string[];
};

export async function generateResponseOptions(
    conversationId: string,
    topics: string[],
    intent: string | null,
): Promise<string[]> {
    const response = await fetch(
        `${CONVERSATIONS_ENDPOINT}/${conversationId}/responses`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                topics,
                intent: intent
                    ? { primary: intent, specific: null }
                    : null,
            }),
        },
    );

    const result: ResponseOptions = await response.json();
    return result.responses;
}
