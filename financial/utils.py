import requests
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from stock.models import Supplier, Item, Inflow, Nomenclature


FORMATO_BANCOS = {
    '341': {
        'agencia': "XXXX",           # Itaú (4 dígitos)
        'conta': "XXXXX-X"           # 5 dígitos + 1 dígito verificador
    },
    '001': {
        'agencia': "XXXX-X",         # Banco do Brasil (4 dígitos + 1 dígito verificador)
        'conta': "XXXXXXXX-X"        # 8 dígitos + 1 dígito verificador
    },
    '237': {
        'agencia': "XXXX-X",         # Bradesco (4 dígitos + 1 dígito verificador)
        'conta': "XXXXXXX-X"         # 7 dígitos + 1 dígito verificador
    },
    '033': {
        'agencia': "XXXX",           # Santander (4 dígitos)
        'conta': "XXXXXXXX-X"        # 8 dígitos + 1 dígito verificador
    },
    '260': {
        'agencia': "XXXX",           # Nubank (4 dígitos)
        'conta': "XXXXXX-X"          # 6 dígitos + 1 dígito verificador
    },
    '336': {
        'agencia': "XXXX",           # C6 Bank (4 dígitos)
        'conta': "XXXXXX-X"          # 6 dígitos + 1 dígito verificador
    },
    '735': {
        'agencia': "XXXX",           # Neon (4 dígitos)
        'conta': "XXXXXX-X"          # 6 dígitos + 1 dígito verificador
    },
    '212': {
        'agencia': "XXXX-X",         # Next (4 dígitos + 1 dígito verificador)
        'conta': "XXXXXX-X"          # 6 dígitos + 1 dígito verificador
    },
    '104': {
        'agencia': "XXXX",           # Caixa Econômica Federal (4 dígitos)
        'conta': "XXXXXXXXXXX-X"     # 11 dígitos + 1 dígito verificador
    },
    '077': {
        'agencia': "XXX",            # Banco Inter (3 dígitos)
        'conta': "XXXX-X"            # 4 dígitos + 1 dígito verificador
    }
}


def formatar_numero(numero, formato):
    """Formata um número com base no formato fornecido."""
    # Remove caracteres não numéricos
    numero = ''.join(filter(str.isdigit, numero))
    
    formatted = []
    contador = 0
    
    for char in formato:
        if char == 'X':
            if contador < len(numero):
                formatted.append(numero[contador])
                contador += 1
        else:
            formatted.append(char)
    
    return ''.join(formatted)

def formatar_agencia_conta(codigo_banco, agencia, conta):
    """Aplica formatação à agência e conta com base no banco selecionado."""
    formatos = FORMATO_BANCOS.get(codigo_banco)
    
    if not formatos:
        # Se não houver um formato definido, retorna os números sem formatação
        return agencia, conta
    
    agencia_formatada = formatar_numero(agencia, formatos['agencia'])
    conta_formatada = formatar_numero(conta, formatos['conta'])
    
    return agencia_formatada, conta_formatada


def buscar_banco_por_codigo(codigo_banco):
    url = f"https://brasilapi.com.br/api/banks/v1/{codigo_banco}"
    response = requests.get(url)
    
    if response.status_code == 200:
        banco = response.json()
        return banco
    else:
        return None
    

def formatar_agencia_conta_ofx(codigo_banco, agencia, numero_conta):
    """Aplica formatação à agência e conta com base no banco selecionado."""
    
    # Obtém os formatos do banco (formato para agência e conta)
    formatos = FORMATO_BANCOS.get(codigo_banco)
    
    if not formatos:
        # Se não houver um formato definido, retorna os números sem formatação
        return agencia, numero_conta

    formato_agencia = formatos['agencia']
    formato_conta = formatos['conta']
    
    # Verifica se o número já está formatado
    if "-" in numero_conta:
        # Se já contém um hífen, assumimos que está formatado corretamente
        return agencia, numero_conta

    # Remove caracteres não numéricos dos formatos para determinar o tamanho esperado
    tamanho_agencia = len(re.sub(r'[^X]', '', formato_agencia))
    tamanho_conta = len(re.sub(r'[^X]', '', formato_conta))

    # Verifica se o número da conta/agência tem o tamanho correto
    if len(numero_conta) != (tamanho_agencia + tamanho_conta):
        raise ValueError("O número da conta não corresponde ao formato esperado.")

    # Separa a parte da agência e da conta do numero_conta fornecido
    agencia = numero_conta[:tamanho_agencia]  # Os primeiros dígitos para a agência
    conta = numero_conta[tamanho_agencia:tamanho_agencia + tamanho_conta]  # O restante para a conta

    # Aplicar a formatação usando as máscaras
    agencia_formatada = aplicar_mascara(formato_agencia, agencia)
    conta_formatada = aplicar_mascara(formato_conta, conta)

    # Retorna a agência e a conta formatadas
    return agencia_formatada, conta_formatada


def aplicar_mascara(formato, numero):
    """Aplica uma máscara de formatação como XXXX-X para um número, se necessário."""
    
    if "-" in numero:
        # Se já estiver formatado, retorna o número diretamente
        return numero

    resultado = ""
    indice_numero = 0

    # Itera sobre os caracteres da máscara, substituindo X pelos dígitos do número
    for char in formato:
        if char == "X":
            # Certifique-se de que não estamos fora dos limites da string 'numero'
            if indice_numero < len(numero):
                resultado += numero[indice_numero]
                indice_numero += 1
            else:
                raise IndexError("Tamanho do número é menor do que o esperado pelo formato.")
        else:
            resultado += char  # Mantém caracteres como '-' ou '.'

    return resultado


def buscar_bankid_no_ofx(ofx_file):
    """
    Função para buscar o BANKID dentro do arquivo OFX.
    :param ofx_file: Arquivo OFX (carregado com FILES)
    :return: O código BANKID encontrado, ou None se não for encontrado
    """
    # Lê o conteúdo do arquivo OFX
    ofx_content = ofx_file.read().decode('utf-8')  # Decodifica o arquivo OFX para string

    # Usando regex para capturar o valor dentro da tag <BANKID>
    bankid_match = re.search(r'<BANKID>(\d+)', ofx_content)

    if bankid_match:
        return bankid_match.group(1)  # Retorna o BANKID encontrado
    else:
        return None  # Retorna None se o BANKID não for encontrado
    


def process_nfe(xml_file, unit):
    namespace = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrai informações da nota fiscal
    nfe_info = {}
    nfe_info['key'] = root.find('.//ns:chNFe', namespace).text
    nfe_info['protocol'] = root.find('.//ns:nProt', namespace).text
    nfe_info['issue_date'] = root.find('.//ns:dhEmi', namespace).text
    nfe_info['due_date'] = root.find('.//ns:dVenc', namespace).text
    nfe_info['description'] = root.find('.//ns:natOp', namespace).text

    # Extrai o valor total da nota
    total = root.find('.//ns:total/ns:ICMSTot', namespace)
    nfe_info['total_value'] = float(total.find('ns:vNF', namespace).text)

    # Pega as informações do fornecedor (emitente)
    emit = root.find('.//ns:emit', namespace)
    supplier = {}
    supplier['name'] = emit.find('ns:xNome', namespace).text
    supplier['cnpj'] = CNPJ_mask(emit.find('ns:CNPJ', namespace).text)

    # Verifica o telefone, email e outros detalhes do fornecedor (emitente)
    ender_emit = emit.find('ns:enderEmit', namespace)
    supplier['phone'] = ender_emit.find('ns:fone', namespace).text if ender_emit.find('ns:fone', namespace) is not None else ''
    supplier['phone'] = phone_mask(supplier['phone'])
    supplier['email'] = emit.find('ns:email', namespace).text if emit.find('ns:email', namespace) is not None else ''
    supplier['contact'] = emit.find('ns:xContato', namespace).text if emit.find('ns:xContato', namespace) is not None else ''
    supplier['address'] = ender_emit.find('ns:xLgr', namespace).text
    supplier['number'] = ender_emit.find('ns:nro', namespace).text
    supplier['neighborhood'] = ender_emit.find('ns:xBairro', namespace).text
    supplier['city'] = ender_emit.find('ns:xMun', namespace).text
    supplier['state'] = ender_emit.find('ns:UF', namespace).text

    # Tenta encontrar ou criar o fornecedor no banco de dados
    try:
        supplier_model = Supplier.objects.get(cnpj=supplier['cnpj'])
    except Supplier.DoesNotExist:
        supplier_model = Supplier.objects.create(
            name=supplier['name'],
            cnpj=supplier['cnpj'],
            address=f"{supplier['address']}, {supplier['number']}, {supplier['neighborhood']}, {supplier['city']}, {supplier['state']}",
            seller=supplier['contact'],
            email=supplier['email'],
            phone_number=supplier['phone']
        )

    nfe_info['supplier'] = supplier_model

    # Extração de itens da NF-e
    unreconciled_items = []
    reconciled_items = []

    for det in root.findall('.//ns:det', namespace):
        item = {}
        item['description'] = det.find('.//ns:xProd', namespace).text
        item['quantity'] = int(float(det.find('.//ns:qCom', namespace).text))
        item['unit_cost'] = float(det.find('.//ns:vUnCom', namespace).text)
        item['total_value'] = float(det.find('.//ns:vProd', namespace).text)
        item['unit'] = det.find('.//ns:uCom', namespace).text

        try:
            # Tenta encontrar o item no estoque pelo nome (nomenclatura)
            nomenclature, created = Nomenclature.objects.get_or_create(name=item['description'])
            exist_item = Item.objects.get(nomenclatures=nomenclature)
            reconciled_items.append(exist_item)

            # Cria a entrada no estoque
            inflow = Inflow.objects.create(
                item=exist_item,
                invoice=nfe_info['key'],
                date=datetime.now(),
                supplier=supplier_model,
                unit=unit,
                target_stock=unit,
                unit_cost=item['unit_cost'],
                quantity=item['quantity'],
                total_cost=item['total_value'],
            )
        except Item.DoesNotExist:
            # Se o item não existe no estoque, adiciona à lista de itens não conciliados
            unreconciled_items.append(item)

    nfe_info['reconciled_items'] = reconciled_items
    nfe_info['unreconciled_items'] = unreconciled_items

    return nfe_info


def CNPJ_mask(cnpj):
    cnpj = ''.join(filter(str.isdigit, cnpj))
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"


def phone_mask(phone):
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) == 10:  # Ex: (99) 9999-9999
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    elif len(phone) == 11:  # Ex: (99) 99999-9999
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    else:
        return phone