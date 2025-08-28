# analise_saude/scripts/gerador_dados.py

import os
import django
import sys
from pathlib import Path
from faker import Faker
from random import randint, choice, uniform
from datetime import datetime, timedelta

# Adiciona o diretório raiz do projeto ao caminho do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observatorio_saude.settings')
django.setup()

from analise_saude.models import NotificacaoDoenca, DadosClimaticos

# Inicializa o Faker
fake = Faker('pt_BR')

# --- Funções de Geração de Dados ---

def gerar_dados_climaticos_ficticios(num_dias):
    """Gera e salva dados climáticos fictícios com variação mais realista."""
    print(f"Gerando dados climáticos para {num_dias} dias...")
    
    data_inicio = datetime.now().date() - timedelta(days=num_dias)
    
    for i in range(num_dias):
        data = data_inicio + timedelta(days=i)
        
        # Simula a variação de temperatura ao longo do ano
        dia_do_ano = data.timetuple().tm_yday
        amplitude_temp = 8  # Variação
        temp_base = 25 - amplitude_temp * (1 - (dia_do_ano / 365) * 2)
        temperatura_media = uniform(temp_base - 3, temp_base + 3)
        
        # Simula a correlação entre temperatura e umidade
        umidade_base = 65 + (temperatura_media - 25) * 2
        
        DadosClimaticos.objects.create(
            data_registro=data,
            temperatura_media=round(temperatura_media, 2),
            precipitacao=randint(0, 50),
            umidade=round(umidade_base + randint(-10, 10), 2)
        )
    print("Dados climáticos gerados com sucesso.")


def gerar_notificacoes_ficticias(num_notificacoes, num_dias_clima):
    """Gera e salva notificações de doenças com base nos dados climáticos."""
    print(f"Gerando {num_notificacoes} notificações de doenças...")
    
    doencas_comuns = ['Dengue', 'Chikungunya', 'Zika', 'Gripe', 'Resfriado']
    regioes_sp = ['Zona Leste', 'Zona Oeste', 'Zona Norte', 'Zona Sul', 'Centro']
    faixas_etarias = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61+']
    sexos = ['Masculino', 'Feminino']

    # Pega todos os dados climáticos gerados para usá-los na correlação
    dados_clima = list(DadosClimaticos.objects.all())
    
    for _ in range(num_notificacoes):
        dado_climatico = choice(dados_clima)
        data_notificacao = dado_climatico.data_registro
        
        # A lógica mais importante:
        # Aumenta a probabilidade de doenças como Dengue e Chikungunya em dias quentes e chuvosos.
        
        doenca = choice(doencas_comuns)
        if dado_climatico.temperatura_media > 28 and dado_climatico.precipitacao > 20:
            if randint(1, 10) > 3: # 70% de chance de ser uma doença ligada ao clima
                doenca = choice(['Dengue', 'Chikungunya'])

        NotificacaoDoenca.objects.create(
            data_notificacao=data_notificacao,
            doenca=doenca,
            regiao=choice(regioes_sp),
            sexo=choice(sexos),
            faixa_etaria=choice(faixas_etarias)
        )
    print("Notificações geradas com sucesso.")


# --- Lógica de Execução Principal ---
if __name__ == "__main__":
    # Limpa os dados existentes
    NotificacaoDoenca.objects.all().delete()
    DadosClimaticos.objects.all().delete()
    
    dias_para_gerar = 730 # Dados de 2 anos
    gerar_dados_climaticos_ficticios(dias_para_gerar)
    
    num_notificacoes = 5000
    gerar_notificacoes_ficticias(num_notificacoes, dias_para_gerar)