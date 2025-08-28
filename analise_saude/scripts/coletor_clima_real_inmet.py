import os
import sys
from pathlib import Path
import requests
import pandas as pd
from datetime import datetime, timedelta
import django

# Adiciona o diretório raiz do projeto ao caminho de busca do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observatorio_saude.settings')
django.setup()

from analise_saude.models import DadosClimaticos

# --- Configurações da API do INMET ---
# Código da estação de Mirante de Santana (SP)
ESTACAO_CODIGO = "A701"

def coletar_dados_climaticos_reais():
    print("Iniciando coleta de dados climáticos reais do INMET...")

    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=365) # Último ano de dados

    url = f"https://apitempo.inmet.gov.br/estacao/{data_inicio.strftime('%Y-%m-%d')}/{data_fim.strftime('%Y-%m-%d')}/{ESTACAO_CODIGO}"

    try:
        # Usamos 'verify=False' para contornar o erro SSL, mas lembre-se que isso não é seguro para produção
        response = requests.get(url, verify=False)
        response.raise_for_status()
        dados = response.json()
        
        for item in dados:
            data_registro = datetime.strptime(item['DT_MEDICAO'], '%Y-%m-%d').date()
            
            temp_min = item.get('TEM_MIN', 0)
            temp_max = item.get('TEM_MAX', 0)
            chuva = item.get('CHUVA', 0)
            umd_min = item.get('UMD_MIN', 0)
            umd_max = item.get('UMD_MAX', 0)

            DadosClimaticos.objects.update_or_create(
                data_registro=data_registro,
                defaults={
                    'temperatura_media': (float(temp_min) + float(temp_max)) / 2,
                    'precipitacao': float(chuva),
                    'umidade': (float(umd_min) + float(umd_max)) / 2
                }
            )
        
        print("Coleta de dados climáticos reais concluída.")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição à API do INMET: {e}")

if __name__ == "__main__":
    coletar_dados_climaticos_reais()
    