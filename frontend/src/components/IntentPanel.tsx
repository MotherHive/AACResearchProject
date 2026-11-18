import { useEffect, useState } from "react"
import type { IntentSelection } from "../services/conversationService";

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
    selectedIntent: IntentSelection | null;
    onSelect: (intent: IntentSelection | null) => void;
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

    const selectedPrimary = intentsData.find((intent) => intent.name === selectedIntent?.primary);
    const primaryThemeIndex = intentsData.findIndex((intent) => intent.name === selectedIntent?.primary);
    const options = selectedPrimary
        ? [
            {
                name: "general",
                label: "General",
                description: selectedPrimary.description,
                selection: { primary: selectedPrimary.name, specific: null },
            },
            ...Object.entries(selectedPrimary.specifics).map(([name, description]) => ({
                name,
                label: name.replaceAll("_", " "),
                description,
                selection: { primary: selectedPrimary.name, specific: name },
            })),
        ]
        : intentsData.map((intent) => ({
            name: intent.name,
            label: intent.name,
            description: intent.description,
            selection: { primary: intent.name, specific: null },
        }));

    return (
        <div>
            <div className="flex flex-wrap items-center justify-between gap-2 my-4 mx-2">
                <h1 className="font-aac font-medium text-2xl">
                    Communication intent{selectedPrimary && <>: <span className="capitalize">{selectedPrimary.name}</span></>}
                </h1>
                {selectedPrimary && (
                    <button
                        type="button"
                        onClick={() => onSelect(null)}
                        className="font-aac text-2xl rounded-xl border-2 border-gray-300 px-4 py-3 hover:bg-gray-100"
                    >
                        Back to intents
                    </button>
                )}
            </div>
            <div className="grid grid-rows-3 grid-cols-2 font-aac font-medium text-4xl gap-4 mx-2">
                {options.map((option, index) => {
                    const theme = pastelThemes[(selectedPrimary ? primaryThemeIndex : index) % pastelThemes.length];
                    const isSelected = selectedIntent?.primary === option.selection.primary
                        && selectedIntent.specific === option.selection.specific;

                    return (
                        <button
                            key={`${option.selection.primary}-${option.name}`}
                            type="button"
                            title={option.description}
                            aria-pressed={isSelected}
                            onClick={() => onSelect(option.selection)}
                            className={`${theme.bg} border-2 ${theme.border} rounded-xl px-2 py-6 content-center text-center hover:brightness-90 transition-all ${
                                isSelected ? "ring-4 ring-blue-500" : ""
                            }`}
                        >
                            <span className="capitalize">{option.label}</span>
                        </button>
                    );
                })}
            </div>
        </div>
    )
}
