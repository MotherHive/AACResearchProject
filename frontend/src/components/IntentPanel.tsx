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
            <h1 className="font-aac font-semibold text-2xl my-2 mx-2">Communication intent</h1>
            <div className="grid grid-rows-3 grid-cols-2 font-aac font-medium text-4xl gap-2 mx-2">
                {intentsData.map((intent) => (
                    <button className="bg-cyan-100 rounded-xl py-6 content-center text-center" key={intent.name}>
                        <h1 className="capitalize">{intent.name}</h1>
                    </button>
                ))}
            </div>
        </div>
    )
}