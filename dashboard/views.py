from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from products.models import Produto, Categoria, MovimentacaoEstoque
from accounts.models import CustomUser
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import ProdutoForm, ImagemProdutoFormSet, CategoriaForm, MovimentacaoEstoqueForm, UsuarioForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Produtos =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

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
    

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Categorias =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class ListarCategorias(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Categoria
    template_name = "dashboard/adm_categoria.html"
    context_object_name = "categorias"

    def test_func(self):
        return self.request.user.is_superuser
    
class CriarCategoria(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categoria
    template_name = "dashboard/criar_categoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy("categorias-adm")

    def test_func(self):
        return self.request.user.is_superuser

class UpdateCategoria(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Categoria
    template_name = "dashboard/criar_categoria.html"
    form_class = CategoriaForm
    success_url = reverse_lazy("categorias-adm")

    def test_func(self):
        return self.request.user.is_superuser

class DeletarCategoria(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Categoria
    template_name = "dashboard/deletar_categoria.html" 
    success_url = reverse_lazy("categorias-adm")

    def test_func(self):
        return self.request.user.is_superuser
    

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Estoque =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class EntradaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "dashboard/movimentacao_estoque.html"
    success_url = reverse_lazy("produtos-adm")

    def get_form_kwargs(self): # função padrão do django que manda o dicionario(kwargs) com todas as informações para iniciar o form
        kwargs = super().get_form_kwargs() # puxa o método da classe mãe(CreateView) que retorna todas as informações necessárias para iniciar o form
        kwargs["tipo_movimentacao"] = "entrada" # adiciona o campo "tipo_movimentação = saida" no kwargs
        return kwargs # manda o kwargs atualizado para o form

    def get_context_data(self, **kwargs): # função padrão do django que manda o dicionario(kwargs) com todas as informações a serem usadas no template
        context = super().get_context_data(**kwargs) # puxa o método da classe mãe(CreateView) que retorna todas as informações necessárias para para o template
        context["tipo_movimentacao"] = "entrada" # adiciona o campo "tipo_movimentação = saida" no context
        return context # manda o context atualizado para o template

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.tipo = "ENTRADA"
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_superuser


class SaidaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = MovimentacaoEstoque
    form_class = MovimentacaoEstoqueForm
    template_name = "dashboard/movimentacao_estoque.html"
    success_url = reverse_lazy("produtos-adm")

    def get_form_kwargs(self): # função padrão do django que manda o dicionario(kwargs) com todas as informações para iniciar o form
        kwargs = super().get_form_kwargs() # puxa o método da classe mãe(CreateView) que retorna todas as informações necessárias para iniciar o form
        kwargs["tipo_movimentacao"] = "saida" # adiciona o campo "tipo_movimentação = saida" no kwargs
        return kwargs # manda o kwargs atualizado para o form

    def get_context_data(self, **kwargs): # função padrão do django que manda o dicionario(kwargs) com todas as informações a serem usadas no template
        context = super().get_context_data(**kwargs) # puxa o método da classe mãe(CreateView) que retorna todas as informações necessárias para para o template
        context["tipo_movimentacao"] = "saida" # adiciona o campo "tipo_movimentação = saida" no context
        return context # manda o context atualizado para o template

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.tipo = "SAIDA"
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.is_superuser
    

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Usuários =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class ListaUsuarios(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'dashboard/adm_usuarios.html'
    context_object_name = 'usuarios'

    def test_func(self):
        return self.request.user.is_superuser
    
class DetalheUsuario(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = CustomUser
    template_name = "dashboard/detalhe_usuario.html"
    context_object_name = "usuario"

    def test_func(self):
        return self.request.user.is_superuser
    
class EditarUsuario(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UsuarioForm
    template_name = "dashboard/editar_usuario.html"
    success_url = reverse_lazy("usuarios-adm")

    def test_func(self):
        return self.request.user.is_superuser