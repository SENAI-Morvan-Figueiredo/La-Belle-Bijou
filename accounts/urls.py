from django.urls import path
from .views import *

urlpatterns = [
    # Página de cadastro
    path('cadastro/', cadastro, name='cadastro'),
    
    # Página de login
    path('login/', login_view, name='login'),
    
    # Logout
    path('logout/', logout_view, name='logout'),

    # Teste de base
    path('base/', teste)
]