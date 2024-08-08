from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from market.models import Order
from point_market_backend.method_mapping import CREATE_ORDER
from zellular import Zellular


class CreateOrderView(APIView):
    def post(self, request):
        # todo: verify data

        # push to zellular
        Zellular.push(CREATE_ORDER, request.data)

        return Response({}, status=status.HTTP_200_OK)


class OrderListView(APIView):
    def get(self, request):
        symbol = request.GET.get('symbol')
        qs = Order.objects.annotate(
            remain_amount=F('amount') - F('filled_amount')
        ).filter(
            symbol__name=symbol,
            remain_amount__gt=0
        )

        data = {
            'buys': qs.filter(name=Order.BUY)[:30],
            'sells': qs.filter(name=Order.SELL)[:30]
        }

        return Response(data, status=status.HTTP_200_OK)
