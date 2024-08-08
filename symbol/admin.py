from django.contrib import admin

from symbol.models import Symbol, Chain, Balance, BalanceModifier

admin.site.register(Symbol)
admin.site.register(Chain)
admin.site.register(Balance)
admin.site.register(BalanceModifier)
