from django.db.models import Max
from django.db.models.functions import Coalesce
from rest_framework import serializers
from web3 import Web3

from market.models import Order
from symbol.models import Symbol, BalanceModifier, Balance


class OrderCreateSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.balance = None
        self.required = None

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'filled_amount')

    def validate(self, attrs):
        user = self.context['user']
        symbol = attrs['symbol']

        nonce = Order.objects.filter(
            user=user,
            symbol=symbol
        ).aggregate(
            max_nonce=Coalesce(Max('nonce'), 0)
        )['max_nonce'] + 1

        if nonce != attrs['nonce']:
            raise serializers.ValidationError("Invalid Nonce")

        name = attrs['name']
        amount = attrs['amount']
        price = attrs['price']

        if name == Order.BUY:
            required = amount * price
            balance = Balance.get_balance_obj(Symbol.get_usdc(), user)
        else:
            required = amount
            balance = Balance.get_balance_obj(symbol, user)

        if balance.value < required:
            raise serializers.ValidationError('Not Enough Balance')

        self.balance = balance
        self.required = required

        return attrs

    def save(self, **kwargs):
        self.balance.decrease(self.required)
        super().save(**kwargs)


class OrderBookSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField(source='remain_amount')

    class Meta:
        model = Order
        fields = ('id', 'amount', 'price')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
