type ResponsePanelProps = {
    responses: string[];
    onSelect: (response: string) => void;
}

export default function ResponsePanel({responses, onSelect}: ResponsePanelProps) {
    return (
        <>
            <section>
                <div className="grid grid-cols-2 grid-rows-2 font-aac font-medium text-2xl text-left gap-4 py-4">
                    {responses.map((response, index) => (
                        <button
                            key={index}
                            onClick={() => onSelect(response)}
                            className="p-4 border rounded-md hover:bg-gray-100 active:bg-gray-200 border-gray-300 border-2 h-30"
                        >
                            {response}
                        </button>

                    ))}
                </div>
            </section>
        </>
    )
}
