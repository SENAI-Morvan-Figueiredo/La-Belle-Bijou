from django.contrib import admin
from .models import Pedido, ItemPedido

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['produto', 'quantidade', 'preco_unitario']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['data_criacao', 'data_final', 'status', 'valor_total'] # campos exibidos na listagem
    list_filter = ['status'] # campo disponivel para filtragem
    search_fields = ['data_criacao', 'data_final', 'status', 'valor_total'] # campos a serem pesquisados na barra de pesquisa

    fieldsets = ( # divide em seções
        ('Datas', {
            'fields': ('data_criacao', 'data_final')
        }),
        ('Informações Gerais', {
            'fields': ('status', 'valor_total')
        }),
    )
    readonly_fields = ['data_criacao', 'valor_total']