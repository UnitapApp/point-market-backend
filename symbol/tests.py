from django.test import TestCase
from eth_account import Account
from rest_framework.test import APIClient

from point_market_backend.management.commands.pull_zellular import PullZellular
from point_market_backend.utils import sign, get_or_create_user
import json

from symbol.methods import withdraw
from symbol.models import Chain, Symbol, Balance


class SymbolTestCase(TestCase):

    def test_create_symbol(self):
        chain = Chain.objects.create(
            name='OP',
            chain_id=10,
            start_block=0,
            last_scanned_block=0
        )

        contract_address_1 = Account.create().address
        function_signature_1 = 'transfer(address,uint256)'
        value_1 = 10

        contract_address_2 = Account.create().address
        function_signature_2 = 'mint()'
        value_2 = 20

        client = APIClient()

        data = json.dumps({
            'name': 'UXP',
            'modifiers': [
                {
                    'chain': chain.id,
                    'contract_address': contract_address_1,
                    'function_signature': function_signature_1,
                    'params_mask': ['*', '*'],
                    'receiver': 0,
                    'value': value_1
                },
                {
                    'chain': chain.id,
                    'contract_address': contract_address_2,
                    'function_signature': function_signature_2,
                    'params_mask': [],
                    'receiver': -1,
                    'value': value_2
                },
            ]
        })

        address, signature = sign(data)

        response = client.post('/api/symbol/create', {
            'address': address,
            'message': data,
            'signature': signature
        }, format='json')
        self.assertEqual(response.status_code, 200)

        PullZellular.perform()

        symbol = Symbol.objects.first()
        self.assertEqual(symbol.name, 'UXP')
    def test_withdraw(self):
        pk = Account.create().key
        account = Account.from_key(pk)
        admin = get_or_create_user(account.address)

        chain = Chain.objects.create(
            name='OP',
            chain_id=10,
            start_block=0,
            last_scanned_block=0
        )

        USDC = Symbol.objects.create(
            name='USDC',
            owner=admin
        )
        Balance.get_balance_obj(USDC, admin).increase(100)

        data = json.dumps({
            'amount': 10
        })
        address, signature = sign(data, private_key=pk)


        withdraw({
            'address': address,
            'message': data,
            'signature': signature
        })


