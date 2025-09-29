from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Produto 
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import ProdutoForm, ImagemProdutoFormSet
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class ListaProdutosAdm(LoginRequiredMixin, UserPassesTestMixin, ListView): 
    model = Produto 
    template_name = "dashboard/adm_produto.html" 
    context_object_name = "produtos"

    def test_func(self):
        return self.request.user.is_superuser


class CriarProduto(LoginRequiredMixin, UserPassesTestMixin, CreateView): # view para criação de produtos
    model = Produto
    form_class = ProdutoForm # formulário a ser renderizado
    template_name = "dashboard/criar_produto.html"

    def get_context_data(self, **kwargs): # método padrão do Django que é chamado toda vez que o template é renderizado
        data = super().get_context_data(**kwargs) # pega o contexto padrão (já contém o form de ProdutoForm) e adiciona o formset(formulários de imagens)
        if self.request.POST:
            data["formset"] = ImagemProdutoFormSet(self.request.POST, self.request.FILES) # Cria o formset já preenchido com os dados enviados e com os arquivos enviados
        else: 
            data["formset"] = ImagemProdutoFormSet() # se for uma requisição GET (primeiro acesso a página) croa o formulário vazio
        return data

    def form_valid(self, form): # método padrão do Django que é chamado toda vez que o formulário é submetido
        context = self.get_context_data() # pega o form e o formset preenchidos
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()              # salva o produto
            formset.instance = self.object         # liga imagens ao produto recém-criado
            formset.save()                         # salva imagens
            return redirect("produtos-adm")        # redireciona
        else:
            return self.form_invalid(form) # se não for válido chama a função com os erros dos formulários
        
    def test_func(self):
        return self.request.user.is_superuser


class UpdateProduto(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Produto
    form_class = ProdutoForm
    template_name = "dashboard/criar_produto.html"

    def get_context_data(self, **kwargs):
        # Pega o contexto padrão (form já carregado com dados do produto)
        data = super().get_context_data(**kwargs)

        if self.request.POST:
            # Se o formulário foi enviado, passa também os arquivos (imagens novas) e associa ao produto
            data["formset"] = ImagemProdutoFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            # Primeira vez carregando a página (GET), carrega com as imagens já salvas
            data["formset"] = ImagemProdutoFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        # Pega o form principal (produto) e o formset (imagens)
        context = self.get_context_data()
        formset = context["formset"]

        if form.is_valid() and formset.is_valid():
            self.object = form.save()  # salva produto atualizado
            formset.instance = self.object
            formset.save()  # salva mudanças nas imagens (add/delete)
            return redirect("produtos-adm")
        else:
            return self.form_invalid(form)
    
    def test_func(self):
        return self.request.user.is_superuser

  
class DeletarProduto(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Produto
    template_name = "dashboard/deletar_produto.html" 
    success_url = reverse_lazy("produtos-adm")

    def test_func(self):
        return self.request.user.is_superuser