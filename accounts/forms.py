from django import forms
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha') # define o campo de senha
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirme a senha") # define o campo de confirmação de senha

    class Meta:
        model = CustomUser # define que esse formulário irá criar/editar instâncias da tabela CustomUser
        fields = ["username", "cpf", "email", "password"] # define a ordem e os campos que irão aparecer
        labels = { # define os labels de cada campo
            "username": "Usuário",
            "cpf": "CPF",
            "email": "E-mail",
        }
        help_texts = { # define os textos de apoio para cada campo
            "username": None,
        }
    
    def clean(self): # função que serve para fazer validações personalizadas antes de salvar o objeto
        cleaned_data = super().clean() # retorna um dicionário com os valores já validados dos campos do formulário
        password = cleaned_data.get("password") # pega o campo de senha do dicionário
        password_confirm = cleaned_data.get("password_confirm") # pega o campo de confimação de senha do dicionário

        if password and password_confirm and password != password_confirm: # verifica se as senhas são diferentes
            self.add_error("password_confirm", "As senhas não coincidem!") # caso forem diferentes retorna o erro

        return cleaned_data # retorna o dicionário para que o django tenha os campos validados
    
    def save(self, commit=True): # sobrescreve o método save padrão para então ser customizado
        user = super().save(commit=False) # cria a instância CustomUser sem salvar no banco
        user.set_password(self.cleaned_data["password"])  # encripta a senha
        if commit:
            user.save() # salva no banco
        return user # retorna o usuário que acaba de ser criado


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True})
    )