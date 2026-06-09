from core.config import settings
from .base import PaymentGateway, PaymentLinkResult, PaymentWebhookResult

PLAN_PRICES = {
    "starter": {"price": 0, "title": "Starter"},
    "corporate": {"price": 49.99, "title": "Corporate"},
    "enterprise": {"price": 199.99, "title": "Enterprise"},
}


class MercadoPagoGateway(PaymentGateway):
    def __init__(self):
        self._client = None

    @property
    def name(self) -> str:
        return "mercadopago"

    def _get_client(self):
        if self._client is None and settings.MERCADO_PAGO_ACCESS_TOKEN:
            import mercadopago
            self._client = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        return self._client

    def is_available(self) -> bool:
        return bool(settings.MERCADO_PAGO_ACCESS_TOKEN)

    def create_payment_link(self, company_name: str, plan: str, email: str, user_id: str, company_id: str, return_url: str) -> PaymentLinkResult:
        client = self._get_client()
        if not client:
            return PaymentLinkResult(success=False, error="Mercado Pago no configurado")

        plan_info = PLAN_PRICES.get(plan, PLAN_PRICES["starter"])
        unit_price = plan_info["price"] if plan_info["price"] > 0 else 0.01

        preference_data = {
            "items": [{
                "title": f"INTELLIWORK™ - Plan {plan_info['title']}",
                "description": f"Suscripción {plan} para {company_name}",
                "quantity": 1,
                "currency_id": "MXN",
                "unit_price": unit_price,
            }],
            "payer": {"email": email},
            "back_urls": {
                "success": return_url,
                "failure": return_url,
                "pending": return_url,
            },
            "auto_return": "approved",
            "external_reference": f"{user_id}|{company_id}|{plan}|{self.name}",
            "notification_url": f"{return_url.rstrip('/')}/api/payments/webhook" if "localhost" not in return_url else "",
            "purpose": "subscription",
        }

        result = client.preference().create(preference_data)
        status = result.get("status")
        if status in (200, 201):
            data = result.get("response", {})
            return PaymentLinkResult(
                success=True,
                payment_id=data.get("id"),
                payment_url=data.get("init_point") or data.get("sandbox_init_point"),
                gateway=self.name,
            )
        return PaymentLinkResult(success=False, error=f"Error MP: {result}")

    def process_webhook(self, body: dict, raw_body: bytes, headers: dict) -> PaymentWebhookResult:
        if body.get("type") == "payment":
            payment_id = body.get("data", {}).get("id")
            if not payment_id:
                return PaymentWebhookResult(success=False)
            client = self._get_client()
            if client:
                payment = client.payment().get(payment_id)
                if payment.get("status") == 200:
                    data = payment.get("response", {})
                    ref = (data.get("external_reference") or "").split("|")
                    if len(ref) >= 3 and data.get("status") == "approved":
                        return PaymentWebhookResult(
                            success=True,
                            user_id=ref[0],
                            company_id=ref[1],
                            plan=ref[2],
                            gateway=self.name,
                            payment_id=str(payment_id),
                        )
        return PaymentWebhookResult(success=False)