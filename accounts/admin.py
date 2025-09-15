from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'cpf', 'data_nasc'] # campos exibidos na listagem
    list_filter = ['data_nasc'] # campo disponivel para filtragem
    search_fields = ['username', 'email', 'cpf', 'data_nasc'] # campos a serem pesquisados na barra de pesquisa

    fieldsets = ( # divide em seções
        ('Identificação', {
            'fields': ('username', 'first_name', 'last_name')
        }),
        ('Informações Gerais', {
            'fields': ('email', 'password', 'cpf', 'data_nasc')
        }),
        ('Dados de Registro', {
            'fields': ('date_joined',)
        }),
    )
    readonly_fields = ['date_joined']