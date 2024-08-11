from django.core.management.base import BaseCommand

from core.models import Config
from point_market_backend.method_mapping import METHODS
from zellular import ZellularStream


class Command(BaseCommand):
    help = "Pulls new requests from zellular"

    def handle(self, *args, **options):
        PullZellular.perform()


class PullZellular:

    @staticmethod
    def perform():
        config = Config.get_config()
        txs, latest_index = ZellularStream.pull(config.last_pulled_index)
        config.last_pulled_index = latest_index
        config.save()
        for tx in txs:
            try:
                METHODS[tx['method']](tx['data'])
            except Exception as e:
                raise e
                # print('Error on running method: ', e)
