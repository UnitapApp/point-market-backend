import heapq
from market.models import Order
from symbol.models import Symbol, Balance


class TradingQueue:
    def __init__(self, symbol, USDC):
        self.buy_orders = []  # Max heap for buy orders, prices negated
        self.sell_orders = []  # Min heap for sell orders
        heapq.heapify(self.buy_orders)
        heapq.heapify(self.sell_orders)
        self.symbol = symbol
        self.USDC = USDC

    def place(self, order: Order):
        name = order.name
        price = order.price
        index = order.id
        if name == Order.BUY:
            heapq.heappush(self.buy_orders, (-price, index, order))
        else:
            heapq.heappush(self.sell_orders, (price, index, order))

    def match(self):
        # Match orders while there are matching orders available
        if not self.buy_orders or not self.sell_orders:
            return False

        # Check if the top buy order matches the top sell order
        buy_price, buy_i, buy_order = self.buy_orders[0]
        sell_price, sell_i, sell_order = self.sell_orders[0]
        buy_price = -buy_price
        if buy_price < sell_price:
            return False

        # Determine the amount to trade
        trade_amount = min(buy_order.remain_amount, sell_order.remain_amount)

        if buy_order.remain_amount > trade_amount:
            buy_order.filled_amount += trade_amount
        else:
            heapq.heappop(self.buy_orders)
            buy_order.filled_amount = buy_order.amount
        buy_order.save()

        if sell_order.remain_amount > trade_amount:
            sell_order.filled_amount += trade_amount
        else:
            heapq.heappop(self.sell_orders)
            sell_order.filled_amount = sell_order.amount
        sell_order.save()

        # Update users balances
        price = sell_price if sell_i < buy_i else buy_price
        buyer_balance: Balance = Balance.get_balance_obj(self.symbol, buy_order.user)
        buyer_balance.increase(trade_amount)
        seller_balance: Balance = Balance.get_balance_obj(self.USDC, sell_order.user)
        seller_balance.increase(price * trade_amount)

        return True
