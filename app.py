from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obter_taxa_de_cambio(base_currency, target_currency):
    url = f'https://api.exchangeratesapi.io/latest?base={base_currency}&symbols={target_currency}'
    response = requests.get(url)
    
    if response.status_code != 200:
        # Tratar o caso em que a API retorna um status diferente de 200
        return None, f"Erro na requisição à API: {response.status_code}"

    dados = response.json()

    if 'rates' not in dados:
        # Tratar o caso em que a chave 'rates' não está presente na resposta
        return None, "Resposta da API não contém a chave 'rates'"

    taxa = dados['rates'][target_currency]
    return taxa, None


def converter_moeda(valor, taxa):
    return valor * taxa

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_currency = request.form['base_currency']
        target_currency = request.form['target_currency']
        amount = float(request.form['amount'])

        taxa = obter_taxa_de_cambio(base_currency, target_currency)
        resultado = converter_moeda(amount, taxa)

        return render_template('index.html', resultado=resultado, base_currency=base_currency, target_currency=target_currency, amount=amount)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
