type TopicTickerProps = {
    topics: string[];
}

export default function TopicTicker({topics} : TopicTickerProps) {
    return (
        <div className="flex flex-row gap-2 justify-center bg-gray-100 py-2 border-y-2 border-gray-300">
            {topics.map((topic, index) => (
                <button key={index} className="font-aac text-3xl font-normal rounded-md border-gray-300 border-2 p-2 bg-white hover:bg-gray-100 hover:border-gray-300 active:bg-gray-200">
                    {topic}
                </button>
            ))}
        </div>
    )
}