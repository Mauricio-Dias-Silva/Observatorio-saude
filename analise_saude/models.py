# analise_saude/models.py
from django.db import models

class NotificacaoDoenca(models.Model):
    """
    Representa uma notificação de caso de doença.
    """
    data_notificacao = models.DateField(help_text="Data da notificação do caso")
    doenca = models.CharField(max_length=100, help_text="Nome da doença (ex: Dengue, Chikungunya)")
    regiao = models.CharField(max_length=100, help_text="Região/bairro onde o caso foi notificado")
    sexo = models.CharField(max_length=10, blank=True, null=True)
    faixa_etaria = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "Notificação de Doença"
        verbose_name_plural = "Notificações de Doenças"
        ordering = ['-data_notificacao']

class DadosClimaticos(models.Model):
    """
    Dados climáticos para correlação.
    """
    data_registro = models.DateField(unique=True, help_text="Data do registro climático")
    temperatura_media = models.FloatField(help_text="Temperatura média diária em graus Celsius")
    precipitacao = models.FloatField(help_text="Total de precipitação diária em mm")
    umidade = models.FloatField(help_text="Umidade relativa do ar média diária")

    class Meta:
        verbose_name = "Dado Climático"
        verbose_name_plural = "Dados Climáticos"
        ordering = ['-data_registro']