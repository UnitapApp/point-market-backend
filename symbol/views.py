from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from point_market_backend.method_mapping import CREATE_SYMBOL
from zellular import Zellular


class SymbolCreateView(APIView):

    def post(self, request, *args, **kwargs):
        # todo: verify data

        # push to zellular
        Zellular.push(CREATE_SYMBOL, request.data)

        return Response({}, status=status.HTTP_200_OK)
