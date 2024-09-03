import locale

# Configure o locale para o formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def format_currency(value):
        # Converte o valor para float e formata como moeda
        return locale.currency(float(value), grouping=True)