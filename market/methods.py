from market.models import Order
from market.serializers import OrderCreateSerializer
from point_market_backend.utils import verify_signature
from symbol.models import Balance, Symbol


def create_order(request_data, save=True) -> Order | None:
    user, data = verify_signature(request_data)

    serializer = OrderCreateSerializer(data=data, context={'user': user})
    serializer.is_valid(raise_exception=True)
    if save:
        serializer.save(
            user=user
        )
        return serializer.instance
