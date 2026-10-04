type TopicTickerProps = {
    topics: string[];
}

export default function TopicTicker({topics} : TopicTickerProps) {
    return (
        <div>
            {topics.map((topic, index) => (
                <span key={index}>
                    {topic}
                </span>
            ))}
        </div>
    )
}