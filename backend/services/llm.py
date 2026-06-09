from typing import Optional
from core.config import settings


class LLMService:
    def __init__(self):
        self._openai = None
        self._anthropic = None
        self._google = None

    @property
    def provider(self) -> Optional[str]:
        if settings.OPENAI_API_KEY:
            return "openai"
        if settings.ANTHROPIC_API_KEY:
            return "anthropic"
        if settings.GOOGLE_API_KEY:
            return "google"
        if settings.GROQ_API_KEY:
            return "groq"
        return None

    def is_available(self) -> bool:
        return self.provider is not None

    def chat(self, system_prompt: str, user_message: str, model: str = None, temperature: float = 0.3) -> Optional[str]:
        provider = self.provider
        if provider == "openai":
            return self._chat_openai(system_prompt, user_message, model or "gpt-4o-mini", temperature)
        elif provider == "anthropic":
            return self._chat_anthropic(system_prompt, user_message, model or "claude-3-haiku-20240307", temperature)
        elif provider == "google":
            return self._chat_google(system_prompt, user_message, model or "gemini-1.5-flash", temperature)
        elif provider == "groq":
            return self._chat_groq(system_prompt, user_message, model or "llama-3.3-70b-versatile", temperature)
        return None

    def _chat_groq(self, system_prompt: str, user_message: str, model: str, temperature: float) -> Optional[str]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                temperature=temperature,
            )
            return resp.choices[0].message.content
        except Exception as e:
            import logging
            logging.error(f"Groq LLM error: {e}")
            return None

    def _chat_openai(self, system_prompt: str, user_message: str, model: str, temperature: float) -> Optional[str]:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                temperature=temperature,
            )
            return resp.choices[0].message.content
        except Exception:
            return None

    def _chat_anthropic(self, system_prompt: str, user_message: str, model: str, temperature: float) -> Optional[str]:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            resp = client.messages.create(
                model=model,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                temperature=temperature,
                max_tokens=2048,
            )
            return resp.content[0].text if resp.content else None
        except Exception:
            return None

    def _chat_google(self, system_prompt: str, user_message: str, model: str, temperature: float) -> Optional[str]:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            model_instance = genai.GenerativeModel(model, system_instruction=system_prompt)
            resp = model_instance.generate_content(user_message, generation_config={"temperature": temperature})
            return resp.text
        except Exception:
            return None


llm = LLMService()
