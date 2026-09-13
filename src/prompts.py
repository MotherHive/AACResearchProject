from main import ResponseContext

PROMPT_BASE='''
'''

PROMPT_NO_INTENT_ADDON='''
'''

PROMPT_INTENT_ADDON='''
'''

PROMPT_TOPICS_ADDON='''
'''

def build_response_prompt(context: ResponseContext) -> str:
    prompt = PROMPT_BASE

    if context.conversation:
        prompt += f"""
        CONVERSATION HISTORY:
        {context.conversation.get_history_str()}
        """

    if context.topics:
        pass

    if context.intent:
        pass