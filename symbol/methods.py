from point_market_backend.utils import verify_signature
from symbol.models import Symbol
from symbol.serializers import SymbolCreateSerializer


def create_symbol(request_data, save=True) -> Symbol:
    user, data = verify_signature(request_data)
    serializer = SymbolCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    if save:
        serializer.save(
            owner=user
        )
    return serializer.instance
