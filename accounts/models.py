from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    telefone = models.CharField(null=True, max_length=15)
    cpf = models.CharField(max_length=11, unique=True)
    data_nasc = models.DateField(null=True, blank=True)
    telefone = models.CharField(null=True, max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "cpf"]

    def __str__(self):
        return self.email

class Endereco(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="enderecos")
    rua = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    cep = models.CharField(max_length=9)
    
    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cep}"