from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from products.models import Produto, ImagemProduto, Categoria, MovimentacaoEstoque
from accounts.models import CustomUser

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Produtos =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class CustomClearableFileInput(ClearableFileInput):
    initial_text = "Imagem atual"
    input_text = "Alterar"
    clear_checkbox_label = "Remover"

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ["nome", "descricao", "preco", "categorias", "imagem_principal"]
        widgets = {
            "imagem_principal": CustomClearableFileInput
        }

    categorias = forms.ModelMultipleChoiceField( # campo categorias é sobrescrito para personalização
        queryset=Produto._meta.get_field("categorias").related_model.objects.all(), # busca todas as categorias disponíveis
        widget=forms.CheckboxSelectMultiple, # define como checkbox
        required=False # permite que o produto seja salvo sem ter categorias
    )

ImagemProdutoFormSet = inlineformset_factory( # cria um formset (conjunto de formulários do mesmo tipo) dentro de outro formulário
    Produto, # model a qual o formset está ligado
    ImagemProduto, # formulários que vão ser criados
    fields=("imagem",), # campos do model ImagemProduto que estarão no formset
    extra=1, # mostra 1 campo inicial
    can_delete=True,
    widgets={"imagem": CustomClearableFileInput},
)


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nome",]


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Estoque =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class MovimentacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ["produto", "quantidade", "motivo"]

    def __init__(self, *args, **kwargs): # método init executado ao criar o formulário
        tipo_movimentacao = kwargs.pop("tipo_movimentacao", None) # tira o campo "tipo_movimentacao" do kwargs caso exista, se não retorna None
        super().__init__(*args, **kwargs)

        if tipo_movimentacao == "entrada": # se o tipo_movimentacao for igual a "entrada"
            self.fields["motivo"].choices = [ # define as opções do campo motivo
                ("COMPRA", "Compra de fornecedor"),
            ]
        elif tipo_movimentacao == "saida": # se o tipo_movimentacao for igual a "saida"
            self.fields["motivo"].choices = [ # define as opções do campo motivo
                ("VENDA", "Venda para cliente"),
            ] 

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Usuarios =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "telefone", "cpf", "data_nasc", "is_active", "is_superuser"]
        labels = {
            "first_name": "Primeiro nome",
            "last_name": "Último nome",
            "data_nasc": "Data de nascimento"
        }

        help_texts = {
            "is_active": None,
            "is_superuser": None,
        }