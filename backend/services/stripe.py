from core.config import settings
from .base import PaymentGateway, PaymentLinkResult, PaymentWebhookResult

PLAN_PRICES = {
    "starter": {"price": 0, "title": "Starter"},
    "corporate": {"price": 4999, "title": "Corporate"},
    "enterprise": {"price": 19999, "title": "Enterprise"},
}


class StripeGateway(PaymentGateway):
    def __init__(self):
        self._client = None

    @property
    def name(self) -> str:
        return "stripe"

    def _get_client(self):
        if self._client is None and settings.STRIPE_SECRET_KEY:
            import stripe as stripe_module
            stripe_module.api_key = settings.STRIPE_SECRET_KEY
            self._client = stripe_module
        return self._client

    def is_available(self) -> bool:
        return bool(settings.STRIPE_SECRET_KEY)

    def create_payment_link(self, company_name: str, plan: str, email: str, user_id: str, company_id: str, return_url: str) -> PaymentLinkResult:
        client = self._get_client()
        if not client:
            return PaymentLinkResult(success=False, error="Stripe no configurado")

        plan_info = PLAN_PRICES.get(plan, PLAN_PRICES["starter"])
        if plan_info["price"] == 0:
            return PaymentLinkResult(success=True, payment_url=return_url, gateway=self.name)

        try:
            price_data = {
                "currency": "usd",
                "product_data": {
                    "name": f"INTELLIWORK™ - Plan {plan_info['title']}",
                    "description": f"Suscripción {plan} para {company_name}",
                },
                "unit_amount": plan_info["price"],
            }
            link = client.PaymentLink.create(
                line_items=[{"price_data": price_data, "quantity": 1}],
                after_completion={"type": "redirect", "redirect": {"url": return_url}},
                metadata={
                    "user_id": user_id,
                    "company_id": company_id,
                    "plan": plan,
                    "gateway": self.name,
                },
            )
            return PaymentLinkResult(
                success=True,
                payment_id=link.id,
                payment_url=link.url,
                gateway=self.name,
            )
        except Exception as e:
            return PaymentLinkResult(success=False, error=f"Error Stripe: {str(e)}")

    def process_webhook(self, body: dict, raw_body: bytes, headers: dict) -> PaymentWebhookResult:
        sig_header = headers.get("stripe-signature")
        if sig_header and settings.STRIPE_WEBHOOK_SECRET:
            try:
                import stripe
                event = stripe.Webhook.construct_event(
                    payload=raw_body,
                    sig_header=sig_header,
                    secret=settings.STRIPE_WEBHOOK_SECRET,
                )
                if event["type"] == "checkout.session.completed":
                    session = event["data"]["object"]
                    metadata = session.get("metadata", {})
                    if session.get("payment_status") == "paid":
                        return PaymentWebhookResult(
                            success=True,
                            user_id=metadata.get("user_id"),
                            company_id=metadata.get("company_id"),
                            plan=metadata.get("plan"),
                            gateway=self.name,
                            payment_id=session.get("id"),
                        )
            except Exception:
                pass
        return PaymentWebhookResult(success=False)