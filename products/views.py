from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Produto
from django.views.generic import TemplateView

class CarrinhoVazio(TemplateView):
    template_name = 'products/vazio.html'

# Create your views here.
class Home(ListView):
    model = Produto
    template_name = "products/home.html"
    context_object_name = "produtos"

class DetailProduto(DetailView):
    model = Produto
    template_name = "products/detalhe_produto.html"
    context_object_name = "produto"