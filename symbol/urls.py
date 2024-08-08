from django.urls import path

from symbol.views import SymbolCreateView, SymbolListView, BalanceView, ChainListView

urlpatterns = [
    path("create", SymbolCreateView.as_view()),
    path("chains", ChainListView.as_view()),
    path("list", SymbolListView.as_view()),
    path("balance", BalanceView.as_view())
]
