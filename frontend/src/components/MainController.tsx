import { useState, useEffect } from 'react';
import TopicTicker from './TopicTicker';
import Keyboard from './Keyboard';
import MicButton from './MicButton';
import { createConversation, createTurn} from '../services/conversationService';

export default function MainController() {
    const [topics, setTopics] = useState<string[]>(['React', 'TypeScript']);
    const [conversationId, setConversationId] = useState<string | null>(null);

    useEffect(() => {
        if (conversationId != null) {
            return;
        }

        createConversation()
            .then((conversation) => {
                setConversationId(conversation.id);
            })
    }, []);

    async function onFinalTranscript(text: string) {
        if (!conversationId) {
            return;
        }

        await createTurn(conversationId, "partner", text)
    }

    return (
        <main>
            {conversationId ? (<MicButton onFinalTranscript={onFinalTranscript}/>) : (<p>Starting the conversation...</p>)}
            <Keyboard/>
            <TopicTicker topics={topics} />
        </main>
    )
}