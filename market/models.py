from django.contrib.auth.models import User
from django.db import models

from symbol.models import Symbol


class Order(models.Model):
    BUY = 'buy'
    SELL = 'sell'

    NAMES = (
        (BUY, 'buy'),
        (SELL, 'sell')
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='orders')
    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE)

    name = models.CharField(choices=NAMES, max_length=4)
    amount = models.BigIntegerField()
    filled_amount = models.BigIntegerField(default=0)
    price = models.BigIntegerField()

    time = models.DateTimeField()
    nonce = models.BigIntegerField()

    @property
    def remain_amount(self):
        return self.amount - self.filled_amount

    def __str__(self):
        return f'{self.id}-{self.user.username}-{self.nonce}'
