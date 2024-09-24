import requests


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