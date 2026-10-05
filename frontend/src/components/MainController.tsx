import { useState, useEffect } from 'react';
import TopicTicker from './TopicTicker';
import MicButton from './MicButton';
import { createConversation, createTurn} from '../services/conversationService';
import Keyboard from './Keyboard';
import IntentPanel from './IntentPanel';

export default function MainController() {
    const [topics, setTopics] = useState<string[]>(['React', 'TypeScript']);
    const [conversationId, setConversationId] = useState<string | null>(null);
    const [topicClue, setTopicClue] = useState<string>("")

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

    function onKeyboardInput(input: string) {
        setTopicClue(input)
    }

    return (
        <main>
            {conversationId ? (<MicButton onFinalTranscript={onFinalTranscript}/>) : (<p>Starting the conversation...</p>)}
            <TopicTicker topics={topics} />
            <section className="grid grid-cols-2">
                <IntentPanel/>
                <Keyboard onInput={onKeyboardInput}/>
            </section>
        </main>
    )
}