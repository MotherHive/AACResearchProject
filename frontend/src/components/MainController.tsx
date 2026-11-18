import { useState, useEffect } from 'react';
import TopicTicker from './TopicTicker';
import MicButton from './MicButton';
import { createConversation, createTurn, generateResponseOptions, generateTopics} from '../services/conversationService';
import type { IntentSelection } from '../services/conversationService';
import Keyboard from './Keyboard';
import IntentPanel from './IntentPanel';
import ResponsePanel from './ResponsePanel';
import { speak } from '../services/speechService';

export default function MainController() {
    const [topics, setTopics] = useState<string[]>([]);
    const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
    const [selectedIntent, setSelectedIntent] = useState<IntentSelection | null>(null);
    const [responses, setResponses] = useState<string[]>([]);
    const [topicClue, setTopicClue] = useState<string>("")
    const [conversationRevision, setConversationRevision] = useState(0);
    const [conversationId, setConversationId] = useState<string | null>(null);

    useEffect(() => {
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
        setConversationRevision((revision) => revision + 1)
    }


    useEffect(() => {
        let current = true;
        const timeout = window.setTimeout(async () => {
            if (!conversationId) {
                return;
            }

            const generatedTopics = await generateTopics(
                conversationId,
                topicClue,
                selectedTopics,
            );

            if (current) {
                setTopics(generatedTopics);
            }

        }, topicClue ? 300 : 0);

        return () => {
            current = false;
            window.clearTimeout(timeout);
        };
    }, [conversationId, topicClue, conversationRevision, selectedTopics]);

    useEffect(() => {
        if (!conversationId) {
            return;
        }

        if (conversationRevision === 0 && selectedTopics.length === 0 && !selectedIntent) {
            return;
        }

        let current = true;

        generateResponseOptions(
            conversationId,
            selectedTopics,
            selectedIntent,
        ).then((generatedResponses) => {
            if (current) {
                setResponses(generatedResponses);
            }
        });

        return () => {
            current = false;
        };
    }, [conversationId, conversationRevision, selectedTopics, selectedIntent]);

    function onKeyboardInput(input: string) {
        setTopicClue(input)
    }

    function onTopicSelect(topic: string) {
        setSelectedTopics((currentTopics) => {
            const alreadySelected = currentTopics.some(
                (selected) => selected.trim().toLowerCase() === topic.trim().toLowerCase(),
            );
            return alreadySelected ? currentTopics : [...currentTopics, topic];
        });
        setTopicClue("");
        setTopics([]);
    }

    function onTopicRemove(topic: string) {
        setSelectedTopics((currentTopics) => currentTopics.filter((selected) => selected !== topic));
    }

    function onTopicSubmit() {
        const topic = topicClue.trim();
        if (topic) {
            onTopicSelect(topic);
        }
    }

    async function onResponseSelect(response: string) {
        if (!conversationId) {
            return;
        }

        await createTurn(conversationId, "user", response);
        await speak(response);
        setConversationRevision((revision) => revision + 1);
        setSelectedTopics([]);
        setSelectedIntent(null);
        setResponses([]);
    }

    return (
        <main>
            {conversationId ? (<MicButton onFinalTranscript={onFinalTranscript}/>) : (<p>Starting the conversation...</p>)}
            <ResponsePanel
                responses={responses}
                onSelect={onResponseSelect}
            />
            <TopicTicker
                topics={topics}
                selectedTopics={selectedTopics}
                onSelect={onTopicSelect}
                onRemove={onTopicRemove}
            />
            <section className="flex flex-row w-full">
                <div className="w-[35%]">
                    <IntentPanel
                        selectedIntent={selectedIntent}
                        onSelect={setSelectedIntent}
                    />
                </div>
                <div className="w-[65%]">
                    <Keyboard input={topicClue} onInput={onKeyboardInput} onSubmit={onTopicSubmit}/>
                </div>
            </section>
        </main>
    )
}
