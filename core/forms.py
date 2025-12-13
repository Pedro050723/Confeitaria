from django import forms
from django.forms import inlineformset_factory
from .models import Pedido, ItemPedido
from .models import Cliente, Produto # Certifique-se que importou Cliente e Produto lá em cima

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'data_entrega', 'hora_entrega', 'local_entrega', 'observacoes_gerais']
        widgets = {
            'data_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_entrega': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observacoes_gerais': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'local_entrega': forms.TextInput(attrs={'class': 'form-control'}),
        }

ItemPedidoFormSet = inlineformset_factory(
    Pedido, ItemPedido,
    # ADICIONAMOS 'preco_no_momento' AQUI:
    fields=('produto', 'quantidade', 'preco_no_momento', 'detalhes'),
    extra=1,
    can_delete=True,
    widgets={
        'produto': forms.Select(attrs={'class': 'form-select'}),
        'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        # Campo novo para editar o preço:
        'preco_no_momento': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'R$ Unitário'}),
        'detalhes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sem glúten'}),
    }
)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email', 'endereco_padrao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco_padrao': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }