import useState from "react"

type ResponsePanelProps = {
}

export default function ResponsePanel(props: ResponsePanelProps) {
    const responses = ["Hi, how are you?", "Good morning!", "I would love to go out to eat later. Where would you want to go?", "Yeah, blue is my favorite color as well."]

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