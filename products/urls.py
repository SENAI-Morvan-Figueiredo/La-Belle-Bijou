from django.urls import path
from .views import Home, DetailProduto

urlpatterns = [
    path('<int:pk>/', DetailProduto.as_view(), name='detalhe-produto'),
]