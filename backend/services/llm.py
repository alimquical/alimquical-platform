from typing import Optional
from core.config import settings


class LLMService:
    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None and settings.OPENAI_API_KEY:
            from openai import OpenAI
            self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        return self._client

    def is_available(self) -> bool:
        return bool(settings.OPENAI_API_KEY)

    def chat(self, system_prompt: str, user_message: str, model: str = "gpt-4o-mini", temperature: float = 0.3) -> Optional[str]:
        client = self._get_client()
        if not client:
            return None
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=temperature,
            )
            return resp.choices[0].message.content
        except Exception:
            return None

    def chat_with_tools(self, system_prompt: str, user_message: str, tools: list[dict], model: str = "gpt-4o-mini"):
        client = self._get_client()
        if not client:
            return None, None
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                tools=tools,
                tool_choice="auto",
                temperature=0.3,
            )
            msg = resp.choices[0].message
            return msg.content, msg.tool_calls
        except Exception:
            return None, None


llm = LLMService()
