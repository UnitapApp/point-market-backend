from django.urls import path

from market.views import CreateOrderView, OrderListView

urlpatterns = [
    path("createOrder", CreateOrderView.as_view()),
    path("orders", OrderListView.as_view())
]
