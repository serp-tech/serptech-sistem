import requests
import re

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