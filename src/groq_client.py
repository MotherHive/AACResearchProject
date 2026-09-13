import os
from groq import Groq
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MODEL = "openai/gpt-oss-120b"
_client = Groq(api_key=os.environ["GROQ_API_KEY"])

def generate_structured[T: BaseModel](prompt: str, response_model: type[T]) -> T:
    response = _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": response_model.__name__,
                "strict": True,
                "schema": response_model.model_json_schema(),
            },
        },
    )
    
    return response_model.model_validate_json(
        response.choices[0].message.content
    )