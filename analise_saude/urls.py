# analise_saude/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notificacoes/', views.lista_notificacoes, name='lista_notificacoes'),
]