import { useEffect, useState } from "react"

type IntentDefinition = {
    description: string;
    specifics: Record<string, string>;
};

type IntentsResponse = {
    intents: Record<string, IntentDefinition>;
};

type IntentItem = IntentDefinition & {
    name: string;
};


export default function IntentPanel() {
    const [intentsData, setIntentsData] = useState<IntentItem[]>([])

    useEffect(() => {
        fetch('http://localhost:8000/api/v1/intents')
            .then((res) => res.json() as Promise<IntentsResponse>)
            .then((json) => {
                const intents = Object.entries(json.intents).map(
                    ([name, definition]) => ({
                        name,
                        ...definition,
                    })
                );

                setIntentsData(intents);
            });
    }, []);


    return (
        <div>
            {intentsData.map((intent) => (
                <div key={intent.name}>
                    <h1>{intent.name}</h1>
                    <p>{intent.description}</p>
                </div>
            ))}
        </div>
    )
}