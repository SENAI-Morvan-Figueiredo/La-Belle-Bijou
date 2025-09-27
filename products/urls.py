from django.urls import path
from .views import *

urlpatterns = [
    path("<int:pk>/", DetailProduto.as_view(), name="detail-produto")
]