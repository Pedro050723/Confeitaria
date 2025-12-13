from django.contrib import admin
from .models import Cliente, Produto, Pedido, ItemPedido

# Configuração simples para mostrar as colunas principais
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email')
    search_fields = ('nome',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'ativo')
    list_filter = ('ativo',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_entrega', 'status', 'total_formatado')
    list_filter = ('status', 'data_entrega')
    
    def total_formatado(self, obj):
        return f"R$ {obj.total:.2f}"
    total_formatado.short_description = 'Total'

# O ItemPedido geralmente a gente não precisa registrar solto, 
# pois ele aparece dentro do Pedido, mas vamos deixar aqui por segurança.
admin.site.register(ItemPedido)