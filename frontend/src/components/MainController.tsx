import { useState, useEffect } from 'react';
import TopicTicker from './TopicTicker';
import MicButton from './MicButton';
import { createConversation, createTurn} from '../services/conversationService';
import Keyboard from './Keyboard';
import IntentPanel from './IntentPanel';
import ResponsePanel from './ResponsePanel';

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
            <ResponsePanel/>
            <TopicTicker topics={topics} />
            <section className="flex flex-row w-full">
                <div className="w-[35%]">
                    <IntentPanel/>
                </div>
                <div className="w-[65%]">
                    <Keyboard onInput={onKeyboardInput}/>
                </div>
            </section>
        </main>
    )
}
