# core/services.py
import gspread
from django.conf import settings
from datetime import datetime

def gerar_recibo_planilha(pedido):
    # 1. Conexão com o Google
    # Certifique-se que o arquivo credentials.json está na pasta raiz do projeto
    gc = gspread.service_account(filename='credentials.json')

    # 2. Abrir a Planilha pelo ID (Peguei do seu print!)
    PLANILHA_ID = '1A20NzPYQ1cnpxcb7ETf5ag_X8L-RTS0N2iH3hHh5ZOQ'
    sh = gc.open_by_key(PLANILHA_ID)

    # 3. Preparar a nova aba
    try:
        template = sh.worksheet("MODELO")
    except:
        return "Erro: Aba 'MODELO' não encontrada na planilha."

    nome_aba = f"Pedido_{pedido.id}"
    
    # Verifica se já existe uma aba com esse nome para não dar erro
    try:
        nova_aba = sh.worksheet(nome_aba)
        # Se já existe, vamos limpar os dados antigos das linhas de itens
        nova_aba.batch_clear(["B14:E22"]) 
    except:
        # Se não existe, duplica o modelo
        nova_aba = template.duplicate(new_sheet_name=nome_aba)

    # 4. Preencher Cabeçalho
    # B10: EMPRESA: [Nome]
    nova_aba.update_acell('B10', f"EMPRESA: {pedido.cliente.nome.upper()}")
    
    # B11: DATA DA ENTREGA: [Data]
    data_fmt = pedido.data_entrega.strftime('%d/%m/%Y')
    nova_aba.update_acell('B11', f"DATA DA ENTREGA: {data_fmt}")

    # 5. Preencher Itens (Loop)
    linha_atual = 14
    itens = pedido.itens.all()

    for item in itens:
        # Descrição (Produto + Obs)
        descricao = item.produto.nome
        if item.detalhes:
            descricao += f" ({item.detalhes})"
        
        # Preço (Garante que é float para o Sheets entender como número)
        preco_unit = float(item.preco_no_momento)
        subtotal = float(item.subtotal)

        # Escreve na linha (Colunas B, C, D, E)
        # Nota: O gspread aceita lista de listas para escrever rápido
        nova_aba.update(f"B{linha_atual}:E{linha_atual}", [[
            descricao, 
            item.quantidade, 
            preco_unit, 
            subtotal
        ]])
        
        linha_atual += 1

    # 6. Preencher Total Final
    # Olhando seu print, o Total parece estar na E25.
    # Se tiver taxa de entrega no futuro, somamos aqui.
    total_pedido = float(pedido.total)
    nova_aba.update_acell('E25', total_pedido)

    # Retorna o link para abrir direto na aba nova
    return f"https://docs.google.com/spreadsheets/d/{PLANILHA_ID}/edit#gid={nova_aba.id}"