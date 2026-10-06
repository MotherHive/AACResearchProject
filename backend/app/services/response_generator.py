from collections.abc import Iterable

from ..db.models import Turn
from .groq import generate_structured
from ..prompts.responses import build_response_prompt
from ..schemas.responses import ResponseDraft, ResponseGenerationRequest, ResponseOptions

def _format_history(turns: Iterable[Turn]) -> str:
    return "\n".join(
        f"{'AAC_USER' if turn.speaker == 'user' else 'PARTNER'}: {turn.text}"
        for turn in turns
    )

def generate_responses(
    turns: Iterable[Turn],
    request: ResponseGenerationRequest,
) -> ResponseOptions:
    recent_turns = list(turns)[-8:]
    latest_turn = recent_turns[-1] if recent_turns else None

    instructions, context = build_response_prompt(
        history=_format_history(recent_turns[:-4]),
        current_exchange=_format_history(recent_turns[-4:-1]),
        latest_turn=_format_history(recent_turns[-1:]),
        latest_speaker=latest_turn.speaker if latest_turn else None,
        request=request,
    )

    draft = generate_structured(
        prompt=context,
        instructions=instructions,
        response_model=ResponseDraft,
    )

    return ResponseOptions(responses=draft.responses)

