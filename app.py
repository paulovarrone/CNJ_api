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

        resultados_extraidos = []

        if 'items' in resultado:
            for item in resultado['items']:

                orgao = item.get('nomeOrgao')
                data_envio = item.get('dataenvio')
                data_disponibilizacao = item.get('datadisponibilizacao')
                tipo_comunicacao = item.get('tipoComunicacao')
                meio = item.get('meiocompleto')
                numero_processo = item.get('numeroprocessocommascara')

                destinatarios = item.get('destinatarios')
                advogados = item.get('destinatarioadvogados')

                if destinatarios:
                    destinatarios_formatado = ', '.join([f"{destinatario['nome']}" for destinatario in destinatarios])
                else:
                    destinatarios_formatado = 'Parte não encontrada'

                if advogados:
                    advogados_formatado = ', '.join([f"{advogado['advogado']['nome']}" for advogado in advogados])
                else:
                    advogados_formatado = 'Advogado não encontrado'
                    
               
            

                resultados_extraidos.append({
                    'numero_processo': numero_processo,
                    'nomeOrgao': orgao, 
                    'dataenvio': data_envio,
                    'datadisponibilizacao': data_disponibilizacao,
                    'tipoComunicacao': tipo_comunicacao,
                    'meiocompleto': meio,
                    'destinatarios': destinatarios_formatado,
                    'destinatarioadvogados': advogados_formatado
                    })

        
        
        return render_template('resultado.html', resultado=resultados_extraidos)

    except requests.RequestException as erro:
       
        return render_template('resultado.html', erro=str(erro))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)























