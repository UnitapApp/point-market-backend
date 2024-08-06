from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from point_market_backend.method_mapping import CREATE_ORDER
from zellular import Zellular


class CreateOrderView(APIView):
    def post(self, request):
        # todo: verify data

        # push to zellular
        Zellular.push(CREATE_ORDER, request.data)

        return Response({}, status=status.HTTP_200_OK)
