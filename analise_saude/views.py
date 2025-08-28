# analise_saude/views.py
from django.shortcuts import render
from django.db.models import Count
from django.core.paginator import Paginator
from datetime import datetime, timedelta
import json
import joblib
import pandas as pd
from django.conf import settings
import os

from .models import NotificacaoDoenca, DadosClimaticos

# Carregar o modelo de IA treinado
try:
    MODELO_PATH = os.path.join(settings.BASE_DIR, 'analise_saude', 'modelo_preditivo.joblib')
    modelo_preditivo = joblib.load(MODELO_PATH)
except FileNotFoundError:
    modelo_preditivo = None

def dashboard(request):
    total_casos = NotificacaoDoenca.objects.count()
    casos_7dias = NotificacaoDoenca.objects.filter(
        data_notificacao__gte=datetime.now() - timedelta(days=7)
    ).count()

    # Lógica para o gráfico de correlação (casos vs. clima)
    correlacao_casos_clima = []
    dados_climaticos_30dias = DadosClimaticos.objects.filter(
        data_registro__gte=datetime.now() - timedelta(days=30)
    ).order_by('data_registro')

    for dado_clima in dados_climaticos_30dias:
        casos_no_dia = NotificacaoDoenca.objects.filter(
            data_notificacao=dado_clima.data_registro
        ).count()
        
        correlacao_casos_clima.append({
            'data': dado_clima.data_registro.strftime('%Y-%m-%d'),
            'temperatura': dado_clima.temperatura_media,
            'precipitacao': dado_clima.precipitacao,
            'casos': casos_no_dia,
        })
    
    # Lógica para o gráfico de tendência de casos
    tendencia_casos_query = NotificacaoDoenca.objects.filter(
        data_notificacao__gte=datetime.now() - timedelta(days=30)
    ).values('data_notificacao').annotate(
        count=Count('id')
    ).order_by('data_notificacao')

    tendencia_casos_list = []
    for item in tendencia_casos_query:
        tendencia_casos_list.append({
            'data_notificacao': item['data_notificacao'].strftime('%Y-%m-%d'),
            'count': item['count']
        })
    
    # Lógica para o gráfico de distribuição de doenças
    distribuicao_doencas_query = NotificacaoDoenca.objects.filter(
        data_notificacao__gte=datetime.now() - timedelta(days=365)
    ).values('doenca').annotate(
        total=Count('id')
    ).order_by('-total')

    # --- Lógica de Previsão de IA ---
    previsao_risco = "Desconhecido"
    if modelo_preditivo:
        dados_recente = DadosClimaticos.objects.order_by('-data_registro').first()
        if dados_recente:
            dados_para_prever = pd.DataFrame({
                'temperatura_media': [dados_recente.temperatura_media],
                'precipitacao': [dados_recente.precipitacao],
                'umidade': [dados_recente.umidade]
            })
            predicao = modelo_preditivo.predict(dados_para_prever)[0]
            previsao_risco = "Alto" if predicao == 1 else "Baixo"

    context = {
        'total_casos': total_casos,
        'casos_7dias': casos_7dias,
        'previsao_risco': previsao_risco,
        'correlacao_casos_clima_json': json.dumps(correlacao_casos_clima), 
        'tendencia_casos_json': json.dumps(tendencia_casos_list),
        'distribuicao_doencas_json': json.dumps(list(distribuicao_doencas_query)),
    }
    return render(request, 'analise_saude/dashboard.html', context)

def lista_notificacoes(request):
    notificacoes_list = NotificacaoDoenca.objects.all().order_by('-data_notificacao')
    doenca = request.GET.get('doenca')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if doenca:
        notificacoes_list = notificacoes_list.filter(doenca=doenca)
    if data_inicio:
        notificacoes_list = notificacoes_list.filter(data_notificacao__gte=data_inicio)
    if data_fim:
        notificacoes_list = notificacoes_list.filter(data_notificacao__lte=data_fim)

    paginator = Paginator(notificacoes_list, 20)
    page_number = request.GET.get('page')
    notificacoes = paginator.get_page(page_number)
    
    doencas_disponiveis = NotificacaoDoenca.objects.values('doenca').annotate(
        total=Count('id')).order_by('doenca')

    context = {
        'notificacoes': notificacoes,
        'doencas_disponiveis': doencas_disponiveis,
    }
    return render(request, 'analise_saude/lista_notificacoes.html', context)