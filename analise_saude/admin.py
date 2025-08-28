from django.contrib import admin
from .models import NotificacaoDoenca, DadosClimaticos

@admin.register(NotificacaoDoenca)
class NotificacaoDoencaAdmin(admin.ModelAdmin):
    list_display = ('data_notificacao', 'doenca', 'regiao')
    list_filter = ('doenca', 'regiao')
    search_fields = ('doenca', 'regiao')

@admin.register(DadosClimaticos)
class DadosClimaticosAdmin(admin.ModelAdmin):
    list_display = ('data_registro', 'temperatura_media', 'precipitacao')
    list_filter = ('data_registro',)
    search_fields = ('data_registro',)