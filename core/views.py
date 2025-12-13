from django.shortcuts import render, redirect
from .models import Pedido
from .forms import PedidoForm, ItemPedidoFormSet
from .forms import ClienteForm, ProdutoForm # Importe os novos forms
from django.shortcuts import render, redirect, get_object_or_404 # Adicione get_object_or_404 nas importações
from django.db.models import Q # <--- IMPORTANTE: Adicione esta linha no TOPO do arquivo
from .services import gerar_recibo_planilha

def dashboard(request):
    pedidos = Pedido.objects.exclude(status='CAN').exclude(status='ENT').order_by('data_entrega')
    query = request.GET.get('q') 
    if query:
        # Filtra por Nome do Cliente OU (Q) pelo ID do pedido
        pedidos = pedidos.filter(
            Q(cliente__nome__icontains=query) | 
            Q(id__icontains=query)
        )

    return render(request, 'dashboard.html', {'pedidos': pedidos})

def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = ItemPedidoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            formset.instance = pedido
            formset.save()
            return redirect('dashboard')
    else:
        form = PedidoForm()
        formset = ItemPedidoFormSet()
    
    context = {
        'form': form, 
        'formset': formset,
        'titulo': 'Registrar Encomenda',
        'botao_texto': 'Salvar Encomenda'
    }

    return render(request, 'novo_pedido.html', {'form': form, 'formset': formset})

def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('novo_pedido') # Depois de criar, já manda pro pedido pra facilitar
    else:
        form = ClienteForm()
    return render(request, 'generico_form.html', {'form': form, 'titulo': 'Novo Cliente'})

def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProdutoForm()
    return render(request, 'generico_form.html', {'form': form, 'titulo': 'Novo Produto'})

def detalhe_pedido(request, pk):
    # Busca o pedido pelo ID (pk) ou dá erro 404 se não existir
    pedido = get_object_or_404(Pedido, pk=pk)
    return render(request, 'detalhe_pedido.html', {'pedido': pedido})

def editar_pedido(request, pk):
    # Pega o pedido existente ou dá erro 404
    pedido = get_object_or_404(Pedido, pk=pk)
    
    if request.method == 'POST':
        # Carrega o form com os dados que vieram da tela (request.POST)
        # MAS avisa que é para atualizar a instância 'pedido' (instance=pedido)
        form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSet(request.POST, instance=pedido)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # Redireciona para os detalhes daquele pedido
            return redirect('detalhe_pedido', pk=pedido.pk)
    else:
        # Carrega o formulário preenchido com os dados do banco
        form = PedidoForm(instance=pedido)
        formset = ItemPedidoFormSet(instance=pedido)
    
    context = {
        'form': form, 
        'formset': formset, 
        'titulo': f'Editar Pedido #{pk}',
        'botao_texto': 'Salvar Alterações'
    }
    return render(request, 'novo_pedido.html', context)

def mudar_status_pedido(request, pk, novo_status):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    # Se o status for válido, salva
    if novo_status in ['PEN', 'PRD', 'ENT', 'CAN']:
        pedido.status = novo_status
        pedido.save()
        
    # Volta para a tela de detalhes
    return redirect('detalhe_pedido', pk=pk)

def gerar_recibo(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    
    try:
        # Chama nosso robô
        link_planilha = gerar_recibo_planilha(pedido)
        
        # Redireciona o usuário para o Google Sheets
        return redirect(link_planilha)
    except Exception as e:
        # Se der erro (ex: credenciais erradas), mostra na tela
        return render(request, 'erro.html', {'mensagem': str(e)})