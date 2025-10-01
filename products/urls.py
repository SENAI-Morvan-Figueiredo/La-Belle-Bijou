from django.urls import path
from .views import Home, DetailProduto, CarrinhoVazio

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<int:pk>/', DetailProduto.as_view(), name='detalhe-produto'),
    path('carrinho/vazio/', CarrinhoVazio.as_view(), name='carrinho-vazio'),
]