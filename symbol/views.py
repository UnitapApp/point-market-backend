from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from point_market_backend.method_mapping import CREATE_SYMBOL
from symbol.models import Chain, Symbol, Balance
from symbol.serializers import ChainListSerializer, SymbolListSerializer, BalanceListSerializer
from zellular import Zellular


class SymbolCreateView(APIView):

    def post(self, request, *args, **kwargs):
        create_symbol(request.data, save=False)

        # push to zellular
        Zellular.push(CREATE_SYMBOL, request.data)

        return Response({}, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        # todo: verify data

        # push to zellular
        Zellular.push(CREATE_SYMBOL, request.data)

        return Response({}, status=status.HTTP_200_OK)


class ChainListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            ChainListSerializer(Chain.objects.all(), many=True).data,
            status=status.HTTP_200_OK
        )

class SymbolListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            SymbolListSerializer(Symbol.objects.all(), many=True).data,
            status=status.HTTP_200_OK
        )


class BalanceView(APIView):
    def get(self, request, *args, **kwargs):
        address = request.GET['address']
        data = BalanceListSerializer(Balance.objects.filter(user__username=address).all(), many=True).data
        return Response(data, status=status.HTTP_200_OK)
