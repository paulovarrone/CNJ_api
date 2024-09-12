from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/resultado')
def resultado():
    
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    nome_parte = request.args.get('nome_parte')
    
    
    url = f"https://hcomunicaapi.cnj.jus.br/api/v1/comunicacao?pagina=1&itensPorPagina=5&data_inicio={data_inicio}&data_fim={data_fim}&nome_parte={nome_parte}"
    
    try:
        
        proxy = {
            'http': 'http://proxy.rio.rj.gov.br:8080',
            'https': 'http://proxy.rio.rj.gov.br:8080'
        }

        
        response = requests.get(url, proxies=proxy, verify=False)
        response.raise_for_status()
        resultado = response.json()

        
        return render_template('resultado.html', resultado=resultado)

    except requests.RequestException as erro:
       
        return render_template('resultado.html', erro=str(erro))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)























