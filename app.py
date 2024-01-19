# app.py

from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obter_taxa_de_cambio(base_currency, target_currency):
    url = f'https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}'
    response = requests.get(url)

    if response.status_code != 200:
        return None, f"Erro na requisição à API: {response.status_code}"

    try:
        dados = response.json()
        taxa = dados['rates'][target_currency]
        return taxa, None
    except KeyError:
        return None, f"A resposta da API não contém a taxa para a moeda de destino '{target_currency}'"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_currency = request.form.get('base_currency')
        target_currency = request.form.get('target_currency')
        amount = float(request.form.get('amount'))

        taxa, erro = obter_taxa_de_cambio(base_currency, target_currency)

        if erro:
            return render_template('erro.html', mensagem=erro)

        resultado = converter_moeda(amount, taxa)

        return render_template('index.html', resultado=resultado, base_currency=base_currency, target_currency=target_currency, amount=amount)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
