from django.urls import path 
from .views import * 

urlpatterns = [ 
    # produtos
    path('produtos/', ListaProdutosAdm.as_view(), name='produtos-adm'),
    path('add-produto/', CriarProduto.as_view(), name="add-produto"),
    path('upd-produto/<int:pk>/', UpdateProduto.as_view(), name="upd-produto"),
    path('delete-produto/<int:pk>/', DeletarProduto.as_view(), name="deletar-produto"),

    # categorias
    path('categorias/', ListarCategorias.as_view(), name="categorias-adm"),
    path('add-categoria/', CriarCategoria.as_view(), name="add-categoria"),
    path('upd-categoria/<int:pk>', UpdateCategoria.as_view(), name="upd-categoria"),
    path('delete-categoria/<int:pk>', DeletarCategoria.as_view(), name="deletar-categoria"),

    # estoque
    path('registrar-entrada/', EntradaCreateView.as_view(), name="add-entrada"),
    path('registrar-saida/', SaidaCreateView.as_view(), name="add-saida"),

    # usuarios
    path('usuarios/', ListaUsuarios.as_view(), name="usuarios-adm")
    ]