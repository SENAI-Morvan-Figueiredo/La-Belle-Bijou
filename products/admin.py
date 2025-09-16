from django.contrib import admin
from .models import Produto, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'preco', 'get_categorias'] 
    list_filter = ['categorias'] 
    search_fields = ['nome', 'descricao']  

    fieldsets = (
        ('Nome', {
            'fields': ('nome',)
        }),
        ('Informações Gerais', {
            'fields': ('descricao', 'preco', 'categorias')
        }),
    )

    def get_categorias(self, obj):
        return ", ".join([c.nome for c in obj.categorias.all()])
    get_categorias.short_description = "Categorias"