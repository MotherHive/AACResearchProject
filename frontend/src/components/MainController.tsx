import { useState } from 'react';
import TopicTicker from './TopicTicker';
import Keyboard from './Keyboard';
import MicButton from './MicButton';

export default function MainController() {
    const [topics, setTopics] = useState<string[]>(['React', 'TypeScript']);

    return (
        <main>
            <MicButton/>
            <Keyboard/>
            <TopicTicker topics={topics} />
        </main>
    )
}