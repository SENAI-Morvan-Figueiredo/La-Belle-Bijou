from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from .models import CustomUser
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.shortcuts import render

class RegisterView(CreateView):
    model = CustomUser # model respectivo
    form_class = RegisterForm # Formulário que será renderizado
    template_name = "accounts/register.html" # Template que será renderizado
    success_url = reverse_lazy("login") # Caso o registro dê certo ele redireciona para a tela de login
    
class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

class CustomLogoutView(LogoutView):
    next_page = "login"

def home(request):
    user = request.user
    return render(request, 'accounts/home.html', {"user": user})
