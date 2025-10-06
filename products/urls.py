from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>/', DetailProduto.as_view(), name='detalhe-produto'),
    path("carrinho/", ver_carrinho, name="ver_carrinho"),
    path("carrinho/adicionar/<int:produto_id>/", adicionar_ao_carrinho, name="adicionar_carrinho"),
    path("carrinho/remover/<int:produto_id>/", remover_do_carrinho, name="remover_carrinho"),
    path("carrinho/limpar/", limpar_carrinho, name="limpar_carrinho"),
    path("carrinho/atualizar-quantidade/", atualizar_quantidade, name="atualizar_quantidade")]