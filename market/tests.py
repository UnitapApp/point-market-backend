from datetime import datetime

from django.test import TestCase
from eth_account import Account
from rest_framework.test import APIClient

from market.management.commands.run_market import RunMarket
from market.models import Order
from core.management.commands.pull_zellular import PullZellular
from point_market_backend.utils import sign, get_or_create_user
import json

from symbol.models import Symbol, Balance


def create_order(private_key, symbol: Symbol, name, amount, price):
    client = APIClient()

    data = json.dumps({
        'symbol': symbol.id,
        'name': name,
        'amount': amount,
        'price': price,
        'time': datetime.now().isoformat(),
        'nonce': 1
    })
    address, signature = sign(data, private_key)
    return client.post('/api/market/createOrder', {
        'address': address,
        'message': data,
        'signature': signature
    }, format='json')


class MarketTestCase(TestCase):

    def test_create_order(self):
        pk1 = Account.create().key
        account1 = Account.from_key(pk1)
        user1 = get_or_create_user(account1.address)

        pk2 = Account.create().key
        account2 = Account.from_key(pk2)
        user2 = get_or_create_user(account2.address)

        USDC = Symbol.objects.create(
            name='USDC',
            owner=user1
        )
        assert USDC.pk == 1

        UXP = Symbol.objects.create(
            name='UXP',
            owner=user1
        )

        AXP = Symbol.objects.create(
            name='AXP',
            owner=user1
        )

        client = APIClient()

        Balance.get_balance_obj(USDC, user1).increase(50)
        response = create_order(pk1, UXP, Order.BUY, 10, 5)
        self.assertEqual(response.status_code, 200)

        Balance.get_balance_obj(UXP, user2).increase(12)
        response = create_order(pk2, UXP, Order.SELL, 5, 4)
        self.assertEqual(response.status_code, 200)

        PullZellular.perform()
        self.assertEqual(Balance.get_balance_obj(USDC, user1).value, 0)
        self.assertEqual(Balance.get_balance_obj(UXP, user2).value, 7)

        RunMarket.run(0)

        self.assertEqual(Balance.get_balance_obj(USDC, user1).value, 0)
        self.assertEqual(Balance.get_balance_obj(USDC, user2).value, 25)
        self.assertEqual(Balance.get_balance_obj(UXP, user1).value, 5)
        self.assertEqual(Balance.get_balance_obj(UXP, user2).value, 7)
