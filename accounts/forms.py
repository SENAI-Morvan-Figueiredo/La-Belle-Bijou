from django import forms
from .models import CustomUser, Endereco
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Senha"}), label='Senha')
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirme a senha"}), label="Confirme a senha")

    class Meta:
        model = CustomUser
        fields = ["username", "cpf", "email", "password"]
        labels = {
            "username": "Usuário",
            "cpf": "CPF",
            "email": "E-mail",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nome de usuário"}),
            "cpf": forms.TextInput(attrs={"placeholder": "CPF"}),
            "email": forms.EmailInput(attrs={"placeholder": "E-mail"}),
        }
        help_texts = {
            "username": None,
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "As senhas não coincidem!")

        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True})
    )

# Novo formulário para edição de perfil
class ProfileForm(forms.ModelForm):
    # Campos do usuário

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'telefone', 'data_nasc', 'cpf']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'data_nasc': 'Data de nascimento',
        }