from time import sleep

from django.core.management.base import BaseCommand
from web3 import Web3

from point_market_backend.rpcs import RPCs
from symbol.models import Chain, BalanceModifier
from symbol.scanner import Scanner


class Scan(BaseCommand):
    help = "Scans blockchain for transactions"

    def handle(self, *args, **options):
        self.run()


    @staticmethod
    def run(block_chuck_size=10, sleep_time=1):
        for chain in Chain.objects.all():
             Scan.run_chain(chain, block_chuck_size, sleep_time)


    @staticmethod
    def run_chain(chain: Chain, block_chuck_size, sleep_time):
        modifiers = BalanceModifier.objects.filter(chain=chain)
        web3 = Web3(Web3.HTTPProvider(RPCs[chain.id]))
        latest_block = web3.eth.block_number
        block_number = chain.last_scanned_block + 1

        scanner = Scanner(web3)

        while block_number <= latest_block:
            transactions = scanner.get_transactions(block_number, min(block_number, latest_block))

            for transaction in transactions:
                for modifier in modifiers:
                    success, params = scanner.process_transaction(transaction, modifier.contract_address, modifier.function_signature, modifier.params)
                    if success:
                        modifier.modify(transaction['from'], params)

            block_number += block_chuck_size
            sleep(sleep_time)

        chain.last_scanned_block = latest_block
        chain.save()
