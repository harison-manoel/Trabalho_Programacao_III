from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from games import views as games_views

urlpatterns = [
    # Painel administrativo do Django
    path('admin/', admin.site.urls),

    # Autenticação e Cadastro de Usuários (Requisitos 2 e 3)
    path('cadastro/', games_views.cadastrar_usuario, name='cadastro'),
    path('login/', games_views.login_view, name='login'),
    path('logout/', games_views.logout_view, name='logout'),

    # Rotas da aplicação de jogos
    path('', include('games.urls', namespace='games')),
]

# Servir arquivos de mídia enviados por upload em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
