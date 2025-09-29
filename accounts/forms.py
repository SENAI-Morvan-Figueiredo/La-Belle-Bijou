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
    phone_number = forms.CharField(
        max_length=20, 
        required=False, 
        label="Número de telefone",
        widget=forms.TextInput(attrs={'placeholder': 'Número de telefone'})
    )
    
    # Campos de endereço
    rua = forms.CharField(
        max_length=255, 
        required=False, 
        label="Rua",
        widget=forms.TextInput(attrs={'placeholder': 'Rua'})
    )
    numero = forms.CharField(
        max_length=10, 
        required=False, 
        label="Número",
        widget=forms.TextInput(attrs={'placeholder': 'Número'})
    )
    complemento = forms.CharField(
        max_length=255, 
        required=False, 
        label="Complemento",
        widget=forms.TextInput(attrs={'placeholder': 'Complemento'})
    )
    cep = forms.CharField(
        max_length=9, 
        required=False, 
        label="CEP",
        widget=forms.TextInput(attrs={'placeholder': 'CEP'})
    )
    bairro = forms.CharField(
        max_length=100, 
        required=False, 
        label="Bairro",
        widget=forms.TextInput(attrs={'placeholder': 'Bairro'})
    )
    cidade = forms.CharField(
        max_length=100, 
        required=False, 
        label="Cidade",
        widget=forms.TextInput(attrs={'placeholder': 'Cidade'})
    )
    estado = forms.CharField(
        max_length=2, 
        required=False, 
        label="Estado (sigla)",
        widget=forms.TextInput(attrs={'placeholder': 'Estado (sigla)', 'maxlength': '2'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preencher os campos com dados existentes
        if self.instance and self.instance.enderecos.exists():
            endereco = self.instance.enderecos.first()
            self.fields['rua'].initial = endereco.rua
            self.fields['numero'].initial = endereco.numero
            self.fields['complemento'].initial = endereco.complemento
            self.fields['cep'].initial = endereco.cep

    def save(self, commit=True):
        user = super().save(commit=commit)
        
        # Salvar ou atualizar o endereço
        if commit:
            endereco_data = {
                'rua': self.cleaned_data.get('rua', ''),
                'numero': self.cleaned_data.get('numero', ''),
                'complemento': self.cleaned_data.get('complemento', ''),
                'cep': self.cleaned_data.get('cep', ''),
            }
            
            if user.enderecos.exists():
                # Atualizar endereço existente
                endereco = user.enderecos.first()
                for field, value in endereco_data.items():
                    setattr(endereco, field, value)
                endereco.save()
            else:
                # Criar novo endereço
                Endereco.objects.create(usuario=user, **endereco_data)
        
        return user