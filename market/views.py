from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from market.methods import create_order
from market.models import Order
from market.serializers import OrderBookSerializer, OrderSerializer
from point_market_backend.method_mapping import CREATE_ORDER
from zellular import ZellularStream


class CreateOrderView(APIView):
    def post(self, request):
        create_order(request.data, save=False)

        # push to zellular
        ZellularStream.push(CREATE_ORDER, request.data)

        return Response({}, status=status.HTTP_200_OK)


class OrderBookView(APIView):
    def get(self, request):
        symbol = request.GET.get('symbol')
        qs = Order.objects.annotate(
            _remain_amount=F('amount') - F('filled_amount')
        ).filter(
            symbol__name=symbol,
            _remain_amount__gt=0
        )

        data = {
            'buys': OrderBookSerializer(qs.filter(name=Order.BUY)[:30], many=True).data,
            'sells': OrderBookSerializer(qs.filter(name=Order.SELL)[:30], many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)


class OrderView(APIView):
    def get(self, request):
        address = request.GET.get('address')
        qs = Order.objects.filter(user__username=address)
        return Response(OrderSerializer(qs, many=True).data, status=status.HTTP_200_OK)
