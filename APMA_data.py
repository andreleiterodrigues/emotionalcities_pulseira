import requests
import os
import json

# Lista dos meses desejados (de agosto a dezembro)
meses = ["08", "09", "10", "11", "12"]

# Código correto da estação meteorológica de Lisboa (Geofísico)
estacao = "1200579"

# Pasta onde os arquivos serão salvos
pasta_destino = "C:/Dados_GPS/Output_APMA/"

# Criando a pasta se não existir
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# Baixando os arquivos para cada mês
for mes in meses:
    # Manter zero à esquerda para a pasta do ano/mês (08, 09, 10...)
    mes_pasta = mes

    # Remover zero à esquerda no nome do arquivo JSON (8, 9, 10...)
    mes_arquivo = str(int(mes))

    url = f"https://api.ipma.pt/public-data/observation/surface-stations/daily_stations/2024/{mes_pasta}/obs_dia_2024_{mes_arquivo}_{estacao}.json"
    resposta = requests.get(url)

    if resposta.status_code == 200:
        try:
            # Testa se o conteúdo da resposta é um JSON válido
            dados = resposta.json()
            
            # Salva o JSON apenas se for válido
            with open(f"{pasta_destino}obs_dia_2024_{mes}_{estacao}.json", "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
            
            print(f"✅ Download concluído: {url}")

        except json.JSONDecodeError:
            print(f"⚠️ Erro: O arquivo de {mes} não é um JSON válido. A resposta pode estar corrompida.")
    else:
        print(f"❌ Erro ao baixar: {url} - Código {resposta.status_code}")
