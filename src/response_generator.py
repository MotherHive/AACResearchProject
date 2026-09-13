from pydantic import BaseModel, ConfigDict, Field
from groq_client import generate_structured
from models import ResponseContext
import prompts

# This is mostly here to be used with the structured generation method.
# The AI model had a tendency of outputting incorrectly structured data.
# Thankfully there is an API option for preventing that. 
class ResponseOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    responses: list[str] = Field(min_length=1, max_length=4)


def generate_responses(
    context: ResponseContext
) -> ResponseOptions:

    prompt = prompts.build_response_prompt(context=context)
    
    responses = generate_structured(
        prompt=prompt, 
        response_model=ResponseOptions
    )

    return responses