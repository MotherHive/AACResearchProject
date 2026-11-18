type TopicTickerProps = {
    topics: string[];
    selectedTopics: string[];
    onSelect: (topic: string) => void;
    onRemove: (topic: string) => void;
}

export default function TopicTicker({topics, selectedTopics, onSelect, onRemove} : TopicTickerProps) {
    return (
        <div className="flex flex-row flex-wrap gap-2 justify-center bg-gray-100 py-2 border-y-2 border-gray-300">
            {selectedTopics.map((topic) => (
                <button
                    key={`selected-${topic}`}
                    type="button"
                    onClick={() => onRemove(topic)}
                    className="font-aac text-3xl font-normal rounded-md border-2 p-2 bg-blue-100 border-blue-500"
                >
                    {topic}
                </button>
            ))}
            {topics.map((topic, index) => (
                <button
                    key={`${topic}-${index}`}
                    type="button"
                    onClick={() => onSelect(topic)}
                    className="font-aac text-3xl font-normal rounded-md border-2 p-2 active:bg-gray-200 bg-white border-gray-300 hover:bg-gray-100"
                >
                    {topic}
                </button>
            ))}
        </div>
    )
}
