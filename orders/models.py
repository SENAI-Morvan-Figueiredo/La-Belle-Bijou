from django.db import models
from accounts.models import CustomUser, Endereco
from products.models import Produto

# Create your models here.
class Pedido(models.Model):
    STATUS_CHOICES = [
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("ENVIADO", "Enviado"),
        ("CANCELADO", "Cancelado"),
    ]

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_final = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDENTE")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, null=False)

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario}"
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido {self.pedido.id})"