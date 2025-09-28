from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, CreateView
from .models import CustomUser
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.shortcuts import render

class RegisterView(CreateView):
    model = CustomUser # model respectivo
    form_class = RegisterForm # Formulário que será renderizado
    template_name = "accounts/cadastro.html" # Template que será renderizado
    success_url = reverse_lazy("login") # Caso o registro dê certo ele redireciona para a tela de login
    
class LoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:  # se for admin
            return reverse_lazy("produtos-adm")  # manda para dashboard admin
        return reverse_lazy("home")  # manda para home normal

class LogoutView(LogoutView):
    next_page = "login"