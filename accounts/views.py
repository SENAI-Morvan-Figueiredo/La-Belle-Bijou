from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from .models import CustomUser
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

# Nova View para edição de perfil
class ProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "accounts/editar_perfil.html"
    success_url = reverse_lazy("profile")
    
    def get_object(self):
        return self.request.user