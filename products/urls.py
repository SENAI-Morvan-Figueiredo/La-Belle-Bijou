from django.urls import path
from .views import Home, DetailProduto

urlpatterns = [
    path('', Home.as_view(), name='home-products'),  # Mudei o nome para evitar conflito
    path('<int:pk>/', DetailProduto.as_view(), name='detalhe-produto'),
]