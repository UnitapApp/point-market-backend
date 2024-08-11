from web3 import Web3

from point_market_backend.rpcs import RPCs
from point_market_backend.utils import verify_signature
from symbol.models import Symbol, Withdraw
# from symbol.operator import PointMarketOperator
from symbol.serializers import SymbolCreateSerializer, WithdrawSerializer
import yaml


def create_symbol(request_data, save=True) -> Symbol:
    user, data = verify_signature(request_data)
    serializer = SymbolCreateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    if save:
        serializer.save(
            owner=user
        )
    return serializer.instance


def withdraw(request_data):
    user, data = verify_signature(request_data)
    serializer = WithdrawSerializer(data=data, context={'user': user})
    serializer.is_valid(raise_exception=True)
    serializer.save(
        user=user
    )

    instance: Withdraw = serializer.instance

    with open("config-files/operator.anvil.yaml", "r") as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)
    # operator = PointMarketOperator(config)
    # operator.process_task_event({
    #     'id': instance.id,
    #     'address': instance.user.username,
    #     'amount': instance.amount,
    #     'block_number': Web3(Web3.HTTPProvider(RPCs[10])).eth.block_number
    # })


    return serializer.instance
