from django.urls import path

from market.views import CreateOrderView, OrderBookView, OrderView

urlpatterns = [
    path("createOrder", CreateOrderView.as_view()),
    path("orderbook", OrderBookView.as_view()),
    path("orders", OrderView.as_view())
]
