import requests
import json


def request_cnpj(cnpj):
    url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
    querystring = {"token": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
                   "cnpj": cnpj, "plugin": "RF"}  # Certifique-se de usar o token correto
    response = requests.request("GET", url, params=querystring)

    if response.status_code == 200:
        resp = json.loads(response.text)
        return {
            'name': resp['nome'],
            'street': resp['logradouro'],
            'number': resp['numero'],
            'complement': resp['complemento'],
            'neighborhood': resp['bairro'],
            'city': resp['municipio'],
            'state': resp['uf'],
            'phone': resp['telefone'],
            'email': resp['email']
        }
    else:
        return None
