from django.urls import path

from market.views import CreateOrderView

urlpatterns = [
    path("createOrder", CreateOrderView.as_view())
]
