import os
import json
import pandas as pd

# Pasta onde estão os arquivos JSON baixados
pasta_json = "C:/Dados_GPS/Output_APMA/"
arquivos = os.listdir(pasta_json)

# Lista para armazenar os dados processados
dados = []

# Processar cada arquivo JSON na pasta
for arquivo in arquivos:
    if arquivo.endswith(".json"):  # Apenas arquivos JSON
        caminho_arquivo = os.path.join(pasta_json, arquivo)

        # Verificar se o arquivo está vazio antes de carregar
        if os.path.getsize(caminho_arquivo) == 0:
            print(f"⚠️ O arquivo {arquivo} está vazio. Pulando...")
            continue  # Pula para o próximo arquivo JSON

        # Carregar o JSON
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()

            if not conteudo:
                print(f"⚠️ O arquivo {arquivo} está completamente vazio. Pulando...")
                continue

            if not (conteudo.startswith("{") or conteudo.startswith("[")):
                print(f"⚠️ O arquivo {arquivo} não contém um JSON válido. Pulando...")
                continue

            try:
                dados_json = json.loads(conteudo)  # Convertendo JSON para dicionário
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao carregar JSON do arquivo {arquivo}: {e}")
                continue  # Se der erro, pula esse arquivo

        # Verificar se o JSON retornou erro
        if "error" in dados_json:
            print(f"⚠️ O arquivo {arquivo} contém uma mensagem de erro do IPMA. Pulando...")
            continue

        # Extraindo dados relevantes
        for registro in dados_json.get("data", []):  # Se não houver "data", retorna lista vazia
            dados.append({
                "Data": registro.get("datetime", "N/A"),  # Data da observação
                "Temperatura Média (°C)": registro.get("Tar_med", None),
                "Temperatura Máx (°C)": registro.get("Tar_max", None),
                "Temperatura Mín (°C)": registro.get("Tar_min", None),
                "Precipitação (mm)": registro.get("RRR_qt", None),
                "Estação": dados_json.get("station_name", "Desconhecida")  # Nome da estação
            })

# Criar DataFrame do Pandas
df = pd.DataFrame(dados)

# Exibir primeiras linhas no terminal
print(df.head())

# Salvar como CSV
df.to_csv("dados_ipma_corrigido.csv", index=False, encoding="utf-8")

# Salvar como Excel
df.to_excel("dados_ipma_corrigido.xlsx", index=False, encoding="utf-8")

print("\n✅ Tabela criada e salva como CSV e Excel!")
