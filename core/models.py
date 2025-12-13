from django.db import models
from django.core.validators import MinValueValidator

class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco_padrao = models.CharField("Endereço Padrão", max_length=255, blank=True, null=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField("Preço Unitário", max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})"

class Pedido(models.Model):
    class StatusPedido(models.TextChoices):
        PENDENTE = 'PEN', 'Pendente'
        EM_PRODUCAO = 'PRD', 'Em Produção'
        ENTREGUE = 'ENT', 'Entregue'
        CANCELADO = 'CAN', 'Cancelado'

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_entrega = models.DateField()
    hora_entrega = models.TimeField()
    local_entrega = models.CharField(max_length=255)
    status = models.CharField(max_length=3, choices=StatusPedido.choices, default=StatusPedido.PENDENTE)
    observacoes_gerais = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_entrega', 'hora_entrega']

    @property
    def total(self):
        return sum(item.subtotal for item in self.itens.all())

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    preco_no_momento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    detalhes = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.preco_no_momento:
            self.preco_no_momento = self.produto.preco
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_no_momento