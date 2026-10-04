import { useState } from 'react';
import TopicTicker from './TopicTicker';
import Keyboard from './Keyboard';

export default function MainController() {
    const [topics, setTopics] = useState<string[]>(['React', 'TypeScript']);

    return (
        <main>
            <Keyboard/>
            <TopicTicker topics={topics} />
        </main>
    )
}