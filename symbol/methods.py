from point_market_backend.utils import verify_signature
from symbol.models import Symbol
from symbol.serializers import SymbolSerializer


def create_symbol(request_data) -> Symbol:
    user, data = verify_signature(request_data)
    serializer = SymbolSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save(
        owner=user
    )
    return serializer.instance
