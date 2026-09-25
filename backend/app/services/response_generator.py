from collections.abc import Iterable

from ..db.models import Turn
from .groq import generate_structured
from ..prompts.responses import build_response_prompt
from ..schemas.responses import ResponseGenerationRequest, ResponseOptions

def _format_history(turns: Iterable[Turn]) -> str:
    return "\n".join(
        f"{turn.speaker}: {turn.text}"
        for turn in turns
    )

def generate_responses(
    turns: Iterable[Turn],
    request: ResponseGenerationRequest,
) -> ResponseOptions:
    prompt = build_response_prompt(
        history=_format_history(turns),
        request=request,
    )

    return generate_structured(
        prompt=prompt,
        response_model=ResponseOptions,
    )



