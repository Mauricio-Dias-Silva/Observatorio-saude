import os
import sys
from pathlib import Path
import requests
from datetime import datetime, timedelta
import django

# Adiciona o diretório raiz do projeto ao caminho de busca do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observatorio_saude.settings')
django.setup()

from analise_saude.models import DadosClimaticos

# --- Configurações da API do INPE/CPTEC ---
CIDADE_CODIGO_SP = 244 

def coletar_dados_climaticos_reais():
    print("Iniciando coleta de dados climáticos reais do INPE...")
    url = f"https://apitempo.inpe.br/previsao/15dias/{CIDADE_CODIGO_SP}"

    try:
        response = requests.get(url, verify=False) # Adicionado verify=False para evitar problemas de SSL
        response.raise_for_status()
        dados = response.json()
        
        for item in dados['previsao']:
            data_registro = datetime.strptime(item['data'], '%Y-%m-%d').date()
            temp_min = item['temperatura_min']
            temp_max = item['temperatura_max']
            
            DadosClimaticos.objects.update_or_create(
                data_registro=data_registro,
                defaults={
                    'temperatura_media': (float(temp_min) + float(temp_max)) / 2,
                    'precipitacao': 0, # A API do INPE/CPTEC não tem precipitação nessa rota
                    'umidade': 70.0 # Valor padrão, a ser ajustado com dados reais
                }
            )
        print("Coleta de dados climáticos reais concluída.")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição à API do INPE: {e}")

if __name__ == "__main__":
    coletar_dados_climaticos_reais()