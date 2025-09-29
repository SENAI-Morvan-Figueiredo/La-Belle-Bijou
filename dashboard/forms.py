from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import ClearableFileInput
from products.models import Produto, ImagemProduto, Categoria

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