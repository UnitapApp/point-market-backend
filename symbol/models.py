import re

from django.contrib.auth.models import User
from django.db import models
from point_market_backend.utils import get_or_create_user


class Symbol(models.Model):
    name = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @staticmethod
    def get_usdc():
        return Symbol.objects.get(name='USDC')

    def __str__(self):
        return self.name


class Chain(models.Model):
    name = models.CharField(max_length=64)
    chain_id = models.IntegerField()
    start_block = models.BigIntegerField()
    last_scanned_block = models.BigIntegerField()


class Balance(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BigIntegerField(default=0)

    @staticmethod
    def get_balance_obj(symbol: Symbol, user: User):
        balance, _ = Balance.objects.get_or_create(
            symbol=symbol,
            user=user
        )
        return balance

    def increase(self, amount):
        self.value += amount
        self.save()

    def decrease(self, amount):
        self.value -= amount
        self.save()

    def __str__(self):
        return f"{self.user.username} : {self.symbol.name} : {self.value}"


class BalanceModifier(models.Model):
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, related_name='modifiers')
    chain = models.ForeignKey(Chain, on_delete=models.PROTECT)

    contract_address = models.CharField(max_length=42)
    function_signature = models.CharField(max_length=255)

    # function call parameters should match params_mask. * is supported
    params_mask = models.JSONField()

    # who should receive the value (-1 for msg.sender, 0 for first param (if it's address), ... )
    receiver = models.IntegerField()

    # which field is value (-1 to use value_amount, 0 for first param (if it's uint/int), ... )
    value = models.IntegerField()
    value_amount = models.BigIntegerField(default=0)

    def get_receiver(self, sender, params):
        if self.receiver == -1:
            return sender
        else:
            return params[self.receiver]

    def get_value(self, params):
        if self.value == -1:
            return self.value_amount
        else:
            return params[self.value]

    def modify(self, sender, params):
        address = self.get_receiver(sender, params)
        user = get_or_create_user(address)

        value = self.get_value(params)

        balance = Balance.get_balance_obj(symbol=self.symbol, user=user)
        if value > 0:
            balance.increase(value)
        else:
            balance.decrease(value)


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    signature = models.JSONField(null=True)
