from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Produto

# Create your views here.
class Home(ListView):
    model = Produto
    template_name = "products/home.html"
    context_object_name = "produtos"

class DetailProduto(DetailView):
    model = Produto
    template_name = "products/detalhe_produto.html"
    context_object_name = "produto"

def teste_carrinho(request):
    return render(request, "products/teste_carrinho.html")