from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomUser
from .forms import RegisterForm, LoginForm, ProfileForm

class RegisterView(CreateView):
    model = CustomUser
    form_class = RegisterForm
    template_name = "accounts/cadastro.html"
    success_url = reverse_lazy("login")
    
class LoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse_lazy("produtos-adm")
        return reverse_lazy("home")

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