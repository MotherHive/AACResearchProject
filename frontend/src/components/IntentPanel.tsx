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

type IntentPanelProps = {
    selectedIntent: string | null;
    onSelect: (intent: string) => void;
};

export default function IntentPanel({selectedIntent, onSelect}: IntentPanelProps) {
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

    const pastelThemes = [
        { bg: "bg-indigo-200/50", border: "border-indigo-500/50" },
        { bg: "bg-emerald-200/50", border: "border-emerald-500/50" },
        { bg: "bg-purple-200/50", border: "border-purple-500/50" },
        { bg: "bg-red-200/50", border: "border-red-500/50" },
        { bg: "bg-amber-200/50", border: "border-amber-500/50" },
        { bg: "bg-cyan-200/50", border: "border-cyan-500/50" },
    ];

    return (
        <div>
            <h1 className="font-aac font-medium text-2xl my-4 mx-2">Communication intent</h1>
            <div className="grid grid-rows-3 grid-cols-2 font-aac font-medium text-4xl gap-4 mx-2">
                {intentsData.map((intent, index) => {
                    const theme = pastelThemes[index % pastelThemes.length];

                    return (
                        <button
                            key={intent.name}
                            onClick={() => onSelect(intent.name)}
                            className={`${theme.bg} border-2 ${theme.border} rounded-xl py-6 content-center text-center hover:brightness-90 transition-all ${
                                selectedIntent === intent.name ? "ring-4 ring-blue-500" : ""
                            }`}
                        >
                            <h1 className="capitalize">{intent.name}</h1>
                        </button>
                    );
                })}
            </div>
        </div>
    )
}
