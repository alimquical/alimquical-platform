from .base import PaymentGateway, PaymentLinkResult, PaymentWebhookResult
from .mercadopago import MercadoPagoGateway

_GATEWAYS: dict[str, PaymentGateway] = {}


def register_gateway(gateway: PaymentGateway):
    _GATEWAYS[gateway.name] = gateway


def get_available_gateways() -> list[PaymentGateway]:
    return [g for g in _GATEWAYS.values() if g.is_available()]


def get_gateway(name: str) -> PaymentGateway | None:
    return _GATEWAYS.get(name)


def get_default_gateway() -> PaymentGateway | None:
    available = get_available_gateways()
    return available[0] if available else None


register_gateway(MercadoPagoGateway())