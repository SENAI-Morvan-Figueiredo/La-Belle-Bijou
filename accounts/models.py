from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    data_nasc = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "cpf"]

    def __str__(self):
        return self.email
