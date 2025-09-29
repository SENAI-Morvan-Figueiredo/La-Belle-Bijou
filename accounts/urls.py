from django.urls import path
from .views import *

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Teste de base
    path('base/', teste)
]