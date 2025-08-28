import os
import django
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from datetime import timedelta
from django.conf import settings
from django.db.models import Count

# Adiciona o diretório raiz do projeto ao caminho de busca do Python
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'observatorio_saude.settings')
django.setup()

from analise_saude.models import NotificacaoDoenca, DadosClimaticos

# --- Fase 1: Coleta e Preparação de Dados ---
def preparar_dados_para_treinamento():
    print("Preparando dados para o modelo...")
    
    # Pega os dados climáticos
    dados_clima = DadosClimaticos.objects.all().order_by('data_registro')
    df_clima = pd.DataFrame(list(dados_clima.values()))
    
    # Adiciona a contagem de casos por dia
    df_casos = pd.DataFrame(list(NotificacaoDoenca.objects.values('data_notificacao').annotate(casos=Count('id'))))
    
    # Unifica os dados de clima e casos
    df = pd.merge(df_clima, df_casos, left_on='data_registro', right_on='data_notificacao', how='left')
    df['casos'] = df['casos'].fillna(0)
    
    # A lógica principal: Criar o rótulo de "surto"
    if len(df) > 0:
        threshold = 5
        df['surto'] = (df['casos'] > threshold).astype(int)
    else:
        print("Não há dados suficientes para treinar o modelo.")
        return None

    # Remove as colunas que não são features
    df = df.drop(columns=['id', 'data_notificacao', 'casos', 'data_registro'])
    
    print(f"Dados preparados. Total de amostras: {len(df)}")
    return df

# --- Fase 2: Treinamento e Avaliação do Modelo ---
def treinar_modelo(df):
    print("Iniciando o treinamento do modelo...")
    
    # Features (Entradas) e Target (Saída)
    features = ['temperatura_media', 'precipitacao', 'umidade']
    target = 'surto'
    
    X = df[features]
    y = df[target]
    
    # Divide os dados para treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Treina o modelo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Avalia o modelo
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {accuracy:.2f}")
    print(f"Relatório de Classificação:\n{classification_report(y_test, y_pred)}")
    
    return model

# --- Fase 3: Salvar o Modelo Treinado ---
def salvar_modelo(model):
    model_path = os.path.join(settings.BASE_DIR, 'analise_saude', 'modelo_preditivo.joblib')
    joblib.dump(model, model_path)
    print(f"Modelo salvo em: {model_path}")

# --- Execução Principal ---
if __name__ == "__main__":
    df = preparar_dados_para_treinamento()
    if df is not None and len(df) > 50:
        modelo_treinado = treinar_modelo(df)
        salvar_modelo(modelo_treinado)
    else:
        print("Não há dados suficientes para treinar o modelo. Por favor, gere dados primeiro.")