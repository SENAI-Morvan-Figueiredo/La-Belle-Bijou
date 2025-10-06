from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
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
    """Adiciona um produto ao carrinho"""
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    cart.add(produto, quantidade=1)
    return redirect("ver_carrinho")

def remover_do_carrinho(request, produto_id):
    """Remove um produto do carrinho"""
    cart = Cart(request)
    produto = get_object_or_404(Produto, id=produto_id)
    cart.remove(produto)
    return redirect("ver_carrinho")

def ver_carrinho(request):
    """Exibe a página do carrinho"""
    cart = Cart(request)
    return render(request, "products/carrinho.html", {"cart": cart})

def limpar_carrinho(request):
    """Limpa todos os itens do carrinho"""
    cart = Cart(request)
    cart.clear()
    return redirect("ver_carrinho")

@require_POST
@csrf_exempt
def atualizar_quantidade(request):
    """Atualiza a quantidade de um produto no carrinho via AJAX"""
    try:
        # Obtém os dados da requisição
        data = json.loads(request.body)
        produto_id = data.get('produto_id')
        quantidade = int(data.get('quantidade'))
        
        cart = Cart(request)
        produto = get_object_or_404(Produto, id=produto_id)
        
        if quantidade > 0:
            # Atualiza a quantidade no carrinho
            cart.add(produto, quantidade=quantidade, override=True)
            
            # Calcula totais atualizados
            total_item = cart.cart[str(produto_id)]['total']
            total_carrinho = cart.get_total_price()
            
            return JsonResponse({
                'success': True,
                'item_total': f"{float(total_item):.2f}",
                'cart_total': f"{float(total_carrinho):.2f}"
            })
        else:
            # Remove o item se quantidade for 0
            cart.remove(produto)
            total_carrinho = cart.get_total_price()
            
            return JsonResponse({
                'success': True,
                'item_total': "0.00",
                'cart_total': f"{float(total_carrinho):.2f}",
                'removed': True
            })
            
    except Exception as e:
        # Retorna erro em caso de exceção
        return JsonResponse({'success': False, 'error': str(e)})