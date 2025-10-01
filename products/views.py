from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Produto
from .cart import Cart

# Create your views here.
class Home(ListView):
    model = Produto
    template_name = "products/home.html"
    context_object_name = "produtos"

class DetailProduto(DetailView):
    model = Produto
    template_name = "products/detalhe_produto.html"
    context_object_name = "produto"

# -=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=--=- Carrinho -=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=--=-

def adicionar_ao_carrinho(request, produto_id):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    cart.add(produto, quantidade=1)
    return redirect("ver_carrinho")

def remover_do_carrinho(request, produto_id):
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    cart.remove(produto)
    return redirect("ver_carrinho")

def ver_carrinho(request):
    cart = Cart(request)
    return render(request, "products/carrinho.html", {"cart": cart})

def limpar_carrinho(request):
    cart = Cart(request)
    cart.clear()
    return redirect("ver_carrinho")