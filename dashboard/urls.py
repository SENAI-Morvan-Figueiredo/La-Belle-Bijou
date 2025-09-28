from django.urls import path 
from .views import * 

urlpatterns = [ 
    path('produtos/', ListaProdutosAdm.as_view(), name='produtos-adm'),
    path('add-produto/', CriarProduto.as_view(), name="add-produto"),
    path('upd-produto/<int:pk>/', UpdateProduto.as_view(), name="upd-produto"),
    path('delete-produto/<int:pk>/', DeletarProduto.as_view(), name="deletar-produto"),
    ]