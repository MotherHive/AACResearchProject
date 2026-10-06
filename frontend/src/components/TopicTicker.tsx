type TopicTickerProps = {
    topics: string[];
    selectedTopics: string[];
    onSelect: (topic: string) => void;
}

export default function TopicTicker({topics, selectedTopics, onSelect} : TopicTickerProps) {
    return (
        <div className="flex flex-row gap-2 justify-center bg-gray-100 py-2 border-y-2 border-gray-300">
            {topics.map((topic, index) => (
                <button
                    key={`${topic}-${index}`}
                    onClick={() => onSelect(topic)}
                    className={`font-aac text-3xl font-normal rounded-md border-2 p-2 active:bg-gray-200 ${
                        selectedTopics.includes(topic)
                            ? "bg-blue-100 border-blue-500"
                            : "bg-white border-gray-300 hover:bg-gray-100"
                    }`}
                >
                    {topic}
                </button>
            ))}
        </div>
    )
}
