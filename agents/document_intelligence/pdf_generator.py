from typing import Optional


class PDFGenerator:
    def generate_report(self, title: str, content: str, output_path: Optional[str] = None) -> bytes:
        return b"[PDF content placeholder]"

    def generate_proposal(self, client_name: str, services: list[dict], total: float) -> bytes:
        return b"[PDF proposal placeholder]"
