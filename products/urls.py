from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', DetailProduto.as_view(), name='detalhe-produto'),
    path('teste', teste_carrinho, name='teste-carrinho')
]