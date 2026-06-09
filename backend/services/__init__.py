from .base import PaymentGateway, PaymentLinkResult, PaymentWebhookResult
from .mercadopago import MercadoPagoGateway
from .stripe import StripeGateway

_GATEWAYS: dict[str, PaymentGateway] = {}

_GATEWAY_PRIORITY = ["stripe", "mercadopago"]


def register_gateway(gateway: PaymentGateway):
    _GATEWAYS[gateway.name] = gateway


def get_available_gateways() -> list[PaymentGateway]:
    available = [g for g in _GATEWAYS.values() if g.is_available()]
    available.sort(key=lambda g: _GATEWAY_PRIORITY.index(g.name) if g.name in _GATEWAY_PRIORITY else 99)
    return available


def get_gateway(name: str) -> PaymentGateway | None:
    return _GATEWAYS.get(name)


def get_default_gateway() -> PaymentGateway | None:
    available = get_available_gateways()
    return available[0] if available else None


register_gateway(MercadoPagoGateway())
register_gateway(StripeGateway())