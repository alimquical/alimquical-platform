from typing import Optional


class MeetingTranscriber:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    async def transcribe(self, audio_path: str) -> str:
        return "[Transcripción simulada - Integrar con Whisper API en producción]"

    async def transcribe_from_bytes(self, audio_bytes: bytes) -> str:
        return "[Transcripción simulada - Integrar con Whisper API en producción]"
