type ResponsePanelProps = {
    responses: string[];
}

export default function ResponsePanel({responses}: ResponsePanelProps) {
    return (
        <>
            <section>
                <div className="grid grid-cols-2 grid-rows-2 font-aac font-medium text-2xl text-left gap-4 py-4">
                    {responses.map((response, index) => (
                        <button key={index} className="p-4 border rounded-md hover:bg-gray-100 active:bg-gray-200 border-gray-300 border-2">
                            {response}
                        </button>

                    ))}
                </div>
            </section>
        </>
    )
}
