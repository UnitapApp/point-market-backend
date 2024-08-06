from django.urls import path

from symbol.views import SymbolCreateView

urlpatterns = [
    path("create", SymbolCreateView.as_view())
]
