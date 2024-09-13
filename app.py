from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/resultado')
def resultado():

    pagina = request.args.get('pagina', 1, type=int)
    
    url = f"https://hcomunicaapi.cnj.jus.br/api/v1/comunicacao"

    params = {
        'numeroOab': request.args.get('numero_oab'),
        'ufOab': request.args.get('uf_oab'),
        'nomeAdvogado': request.args.get('nome_advogado'),
        'nomeParte': request.args.get('nome_parte'),
        'numeroProcesso': request.args.get('numero_processo'),
        'dataDisponibilizacaoInicio': request.args.get('data_inicio'),
        'dataDisponibilizacaoFim': request.args.get('data_fim'),
        'pagina': pagina,
        'itensPorPagina': 10
    }
    
    try:
        
        proxy = {
            'http': None,
            'https': None
        }

        
        response = requests.get(url,params=params, proxies=proxy)
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

        total_items = resultado.get('count', 0)
        itens_por_pagina = 10 
        total_paginas = (total_items // itens_por_pagina) + (1 if total_items % itens_por_pagina else 0)
        
        return render_template('resultado.html', resultado=resultados_extraidos, pagina=pagina, total_paginas=total_paginas)

    except Exception as e:
       
        return render_template('resultado.html', erro=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)























