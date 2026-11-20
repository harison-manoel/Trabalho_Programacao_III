from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # Página Inicial pública
    path('', views.index, name='index'),

    # Ações de Jogos
    path('jogo/cadastrar/', views.cadastrar_jogo, name='cadastrar_jogo'),
    path('jogo/<slug:slug>/', views.detalhe_jogo, name='detalhe'),
    path('jogo/<slug:slug>/editar/', views.editar_jogo, name='editar_jogo'),
    path('jogo/<slug:slug>/deletar/', views.deletar_jogo, name='deletar_jogo'),

    # Avaliações
    path('jogo/<slug:slug>/avaliar/', views.adicionar_avaliacao, name='adicionar_avaliacao'),
    path('avaliacao/<int:id>/deletar/', views.deletar_avaliacao, name='deletar_avaliacao'),

    # Painel do usuário
    path('meus-jogos/', views.meus_jogos, name='meus_jogos'),
]
