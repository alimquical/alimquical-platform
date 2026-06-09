from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentLinkResult:
    success: bool
    payment_id: Optional[str] = None
    payment_url: Optional[str] = None
    gateway: Optional[str] = None
    error: Optional[str] = None


@dataclass
class PaymentWebhookResult:
    success: bool
    user_id: Optional[str] = None
    company_id: Optional[str] = None
    plan: Optional[str] = None
    gateway: Optional[str] = None
    payment_id: Optional[str] = None


class PaymentGateway:
    @property
    def name(self) -> str:
        raise NotImplementedError

    def is_available(self) -> bool:
        return False

    def create_payment_link(
        self,
        company_name: str,
        plan: str,
        email: str,
        user_id: str,
        company_id: str,
        return_url: str,
    ) -> PaymentLinkResult:
        raise NotImplementedError

    def process_webhook(self, body: dict, headers: dict) -> PaymentWebhookResult:
        raise NotImplementedError