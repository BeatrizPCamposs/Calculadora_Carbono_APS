from flask import Flask, render_template, request

app = Flask(__name__)  # Cria uma instância do aplicativo Flask

@app.route('/')  # Define a rota para a página inicial
def index():
    return render_template('index.html')  # Renderiza o template index.html

@app.route('/calcular', methods=['POST'])  # Define a rota para o cálculo, permitindo apenas métodos POST
def calcular():
    try:
        # Dicionário que mapeia regiões do Brasil para seus estados
        regioes = { 
            "Norte": ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins"],
            "Nordeste": ["Alagoas", "Bahia", "Ceará", "Maranhão", "Paraíba", "Pernambuco", "Piauí", "Rio Grande do Norte", "Sergipe"],
            "Centro-Oeste": ["Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"],
            "Sudeste": ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"],
            "Sul": ["Paraná", "Rio Grande do Sul", "Santa Catarina"]
        }

        # Dicionário que armazena as tarifas médias de eletricidade por região
        tarifas = { 
            "Norte": 0.80, 
            "Nordeste": 0.75, 
            "Centro-Oeste": 0.78,
            "Sudeste": 0.85, 
            "Sul": 0.82
        }

        estado = request.form.get('estado')  # Obtém o estado informado no formulário
        if not estado:
            raise ValueError("Estado não informado.")  # Verifica se o estado foi informado

        # Determina a região com base no estado informado
        regiao = next((r for r, estados in regioes.items() if estado in estados), None)
        if not regiao:
            raise ValueError("Estado inválido.")  # Erro se o estado não está nas regiões definidas

        tarifa_media = tarifas[regiao]  # Obtém a tarifa média da região
        consumo_kwh = request.form.get('consumo_kwh')  # Obtém o consumo de eletricidade em kWh
        valor_reais = request.form.get('valor_reais')  # Obtém o valor em reais da eletricidade

        # Converte o consumo para float se informado, caso contrário, calcula a partir do valor em reais
        if consumo_kwh:
            consumo_kwh = float(consumo_kwh)
        elif valor_reais:
            valor_reais = float(valor_reais)
            consumo_kwh = valor_reais / tarifa_media  # Cálculo de consumo com base no valor e tarifa
        else:
            raise ValueError("Consumo de eletricidade não informado.")  # Erro se nenhum valor for informado

        fator_emissao_eletricidade = 0.1  # kg CO₂ por kWh
        pegada_carbono_eletricidade = consumo_kwh * fator_emissao_eletricidade  # Calcula a pegada de carbono da eletricidade

        # Obtém o consumo de gás
        consumo_botijao = request.form.get('consumo_botijao')
        consumo_gas_encanado = request.form.get('consumo_gas_encanado')

        # Fatores de emissão para gás
        fator_emissao_botijao = 25.09  # kg de CO₂ por botijão
        fator_emissao_gas_encanado = 2.04  # kg de CO₂ por m³ de gás encanado

        pegada_carbono_gas = 0  # Inicializa a variável da pegada de carbono do gás
        if consumo_botijao:
            consumo_botijao = float(consumo_botijao)
            pegada_carbono_gas += consumo_botijao * fator_emissao_botijao  # Calcula a pegada de carbono do botijão

        if consumo_gas_encanado:
            consumo_gas_encanado = float(consumo_gas_encanado)
            pegada_carbono_gas += consumo_gas_encanado * fator_emissao_gas_encanado  # Calcula a pegada de carbono do gás encanado

        # Obtém informações sobre combustível
        tipo_combustivel = request.form.get('tipo_combustivel')
        consumo_combustivel = request.form.get('consumo_combustivel')
        valor_combustivel = request.form.get('valor_combustivel')

        # Fatores de emissão e preços dos combustíveis
        fator_emissao_particular = { 
            "gasolina": 2.31,
            "diesel": 2.68,
            "cng": 2.75,
            "etanol": 1.93
        }
        precos_combustivel = { 
            "gasolina": 6.09,
            "diesel": 5.94,
            "cng": 3.50,
            "etanol": 4.04
        }

        pegada_carbono_particular = 0  # Inicializa a variável da pegada de carbono de combustível
        if tipo_combustivel in fator_emissao_particular:
            fator_emissao = fator_emissao_particular[tipo_combustivel]  # Obtém o fator de emissão para o tipo de combustível
            preco_combustivel = precos_combustivel[tipo_combustivel]  # Obtém o preço do combustível

            # Calcula o consumo de combustível
            if consumo_combustivel:
                consumo_combustivel = float(consumo_combustivel)
            elif valor_combustivel:
                valor_combustivel = float(valor_combustivel)
                consumo_combustivel = valor_combustivel / preco_combustivel  # Cálculo de consumo a partir do valor
            else:
                raise ValueError("Consumo de combustível não informado.")  # Erro se nenhum valor for informado

            pegada_carbono_particular += consumo_combustivel * fator_emissao  # Calcula a pegada de carbono do combustível

        # Obtém o número de viagens aéreas
        viagens_nacionais = request.form.get('viagens_nacionais')
        viagens_internacionais = request.form.get('viagens_internacionais')

        # Fatores de emissão para viagens
        fator_emissao_nacional = 106.1  # kg de CO₂ por viagem nacional
        fator_emissao_internacional = 255.0  # kg de CO₂ por viagem internacional

        pegada_carbono_aereo = 0  # Inicializa a variável da pegada de carbono de viagens
        if viagens_nacionais:
            viagens_nacionais = int(viagens_nacionais)
            pegada_carbono_aereo += viagens_nacionais * fator_emissao_nacional  # Calcula a pegada de carbono de viagens nacionais

        if viagens_internacionais:
            viagens_internacionais = int(viagens_internacionais)
            pegada_carbono_aereo += viagens_internacionais * fator_emissao_internacional  # Calcula a pegada de carbono de viagens internacionais

        # Adicionando a pegada de carbono dos resíduos e carne bovina
        consumo_residuos = request.form.get('residuos_gerados')
        consumo_carne = request.form.get('consumo_carne')

        # Fatores de emissão para resíduos e carne
        fator_emissao_residuos = 0.5  # kg CO₂ por kg de resíduos
        fator_emissao_carne = 70.0  # kg CO₂ por kg de carne

        pegada_carbono_residuos = 0  # Inicializa a variável da pegada de carbono dos resíduos
        if consumo_residuos:
            consumo_residuos = float(consumo_residuos)
            pegada_carbono_residuos += consumo_residuos * fator_emissao_residuos  # Calcula a pegada de carbono dos resíduos

        pegada_carbono_carne = 0  # Inicializa a variável da pegada de carbono da carne
        if consumo_carne:
            consumo_carne = float(consumo_carne)
            pegada_carbono_carne += consumo_carne * fator_emissao_carne  # Calcula a pegada de carbono da carne

        # Calcula a pegada total de carbono
        total_pegada_carbono = (
            pegada_carbono_eletricidade +
            pegada_carbono_gas +
            pegada_carbono_particular +
            pegada_carbono_aereo +
            pegada_carbono_residuos +
            pegada_carbono_carne
        ) / 1000  # Convertendo para toneladas

        # Ajusta o cálculo da média anual
        total_media_anual = total_pegada_carbono / 12 if total_pegada_carbono > 0 else 0

        # Retorna todas as variáveis para o template
        return render_template('index.html', 
                               total_pegada=total_pegada_carbono, 
                               total_media=total_media_anual,
                               pegada_eletricidade=pegada_carbono_eletricidade,
                               pegada_gas=pegada_carbono_gas,
                               pegada_particular=pegada_carbono_particular,
                               pegada_residuos=pegada_carbono_residuos,
                               pegada_carne=pegada_carbono_carne,
                               pegada_aereo=pegada_carbono_aereo)

    except Exception as e:
        # Retorna erro em caso de exceção
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)  # Executa o aplicativo Flask
