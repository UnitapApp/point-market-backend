"""
URL configuration for point_market_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

from market.management.commands.run_market import RunMarket
from core.management.commands.pull_zellular import PullZellular
from symbol.management.commands.scan import Scan


@api_view(['GET'])
def run_crons(request):

    try:
        RunMarket.run(0)
    except Exception as e:
       pass

    try:
        PullZellular.perform()
    except Exception as e:
       pass

    try:
        Scan.run()
    except Exception as e:
        pass

    return Response({})


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/symbol/", include("symbol.urls")),
    path("api/market/", include("market.urls")),
    path('run-crons/', run_crons),
]
