from django.contrib import admin
from .models import Categoria, Jogo, Avaliacao


class AvaliacaoInline(admin.TabularInline):
    model = Avaliacao
    extra = 0
    fields = ('usuario', 'nota', 'titulo', 'recomenda', 'criado_em')
    readonly_fields = ('criado_em',)
    show_change_link = True


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'icone', 'total_jogos', 'criado_em')
    search_fields = ('nome', 'descricao')
    prepopulated_fields = {'slug': ('nome',)}
    list_per_page = 20

    def total_jogos(self, obj):
        return obj.jogos.count()
    total_jogos.short_description = "Qtd. de Jogos"


@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'categoria',
        'desenvolvedora',
        'plataforma',
        'preco',
        'criado_por',
        'media_avaliacoes',
        'destaque',
        'criado_em'
    )
    list_filter = ('categoria', 'destaque', 'plataforma', 'data_lancamento')
    search_fields = ('titulo', 'desenvolvedora', 'distribuidora', 'descricao')
    prepopulated_fields = {'slug': ('titulo',)}
    autocomplete_fields = ('categoria', 'criado_por')
    inlines = [AvaliacaoInline]
    date_hierarchy = 'data_lancamento'
    list_per_page = 25
    fieldsets = (
        ('Identificação do Jogo', {
            'fields': ('titulo', 'slug', 'categoria', 'criado_por', 'destaque')
        }),
        ('Produção e Lançamento', {
            'fields': ('desenvolvedora', 'distribuidora', 'plataforma', 'data_lancamento', 'preco')
        }),
        ('Mídias e Links', {
            'fields': ('imagem', 'imagem_url', 'trailer_url', 'site_oficial')
        }),
        ('Descrição', {
            'fields': ('descricao',)
        }),
    )


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('jogo', 'usuario', 'nota', 'titulo', 'recomenda', 'criado_em')
    list_filter = ('nota', 'recomenda', 'criado_em')
    search_fields = ('titulo', 'comentario', 'jogo__titulo', 'usuario__username')
    autocomplete_fields = ('jogo', 'usuario')
    readonly_fields = ('criado_em', 'atualizado_em')
    list_per_page = 30
