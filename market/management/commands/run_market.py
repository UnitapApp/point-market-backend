from time import sleep

from django.core.management.base import BaseCommand
from django.db.models import Q, F

from market.market import TradingQueue
from market.models import Order
from symbol.models import Symbol


class Command(BaseCommand):
    help = "Runs market to start matching orders"

    def handle(self, *args, **options):
        RunMarket.run(t=0)


class RunMarket:
    @staticmethod
    def run(t):
        USDC = Symbol.get_usdc()
        trading_queues = {}
        for symbol in Symbol.objects.filter(pk__gt=1).all():
            trading_queues[symbol] = TradingQueue(
                symbol=symbol,
                USDC=USDC,
            )

        last_order = None
        while True:
            last_order = RunMarket.place_orders(trading_queues, last_order)
            for symbol, trading_queue in trading_queues.items():
                while trading_queue.match(): pass

            if t > 0:
                sleep(t)
            else:
                break

    @staticmethod
    def place_orders(trading_queues, last_order=None):
        orders = Order.objects.filter(
            ~Q(amount=F('filled_amount'))
        ).order_by('id')

        if last_order:
            orders = orders.filter(id__gt=last_order.id)

        for order in orders:
            trading_queues[order.symbol].place(order)

        return orders.last()
