import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg


class Categoria(models.Model):
    """
    Tabela 1: Categorias/Gêneros de jogos (ex: RPG, Ação, Indie, etc.)
    """
    nome = models.CharField(max_length=60, unique=True, verbose_name="Nome da Categoria")
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    icone = models.CharField(
        max_length=50,
        default="bi-controller",
        help_text="Classe de ícone Bootstrap Icons (ex: bi-controller, bi-fire, bi-shield, bi-joystick)",
        verbose_name="Ícone Bootstrap"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    """
    Tabela 2: Informações principais do Jogo.
    Possui chave estrangeira para Categoria e para User (Django auth.User).
    """
    PLATAFORMAS_CHOICES = [
        ('PC', 'PC (Windows/Linux/Mac)'),
        ('PlayStation 5', 'PlayStation 5'),
        ('PlayStation 4', 'PlayStation 4'),
        ('Xbox Series X/S', 'Xbox Series X/S'),
        ('Xbox One', 'Xbox One'),
        ('Nintendo Switch', 'Nintendo Switch'),
        ('Multiplataforma', 'Multiplataforma'),
        ('Mobile', 'Mobile (Android/iOS)'),
    ]

    titulo = models.CharField(max_length=150, verbose_name="Título do Jogo")
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='jogos',
        verbose_name="Categoria / Gênero"
    )
    criado_por = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='jogos_cadastrados',
        verbose_name="Cadastrado por (Usuário)"
    )
    desenvolvedora = models.CharField(max_length=120, verbose_name="Desenvolvedora / Estúdio")
    distribuidora = models.CharField(max_length=120, blank=True, verbose_name="Distribuidora (Publisher)")
    plataforma = models.CharField(max_length=150, default='Multiplataforma', verbose_name="Plataforma(s)")
    data_lancamento = models.DateField(verbose_name="Data de Lançamento")
    preco = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00,
        verbose_name="Preço Sugerido (R$)",
        help_text="Insira 0.00 para jogos gratuitos / Free to Play"
    )
    descricao = models.TextField(verbose_name="Sinopse e Detalhes")
    imagem = models.ImageField(
        upload_to='capas/',
        blank=True,
        null=True,
        verbose_name="Upload da Imagem de Capa"
    )
    imagem_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="URL Direta da Capa (Opcional)",
        help_text="Se preferir, insira uma URL direta de imagem da internet"
    )
    trailer_url = models.URLField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Link do Trailer (YouTube)",
        help_text="Exemplo: https://www.youtube.com/watch?v=VIDEO_ID"
    )
    site_oficial = models.URLField(
        blank=True,
        null=True,
        verbose_name="Site Oficial / Loja (Steam, Epic, etc.)"
    )
    destaque = models.BooleanField(default=False, verbose_name="Em Destaque no Portal?")
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")

    class Meta:
        verbose_name = "Jogo"
        verbose_name_plural = "Jogos"
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titulo)
            slug = base_slug
            contador = 1
            while Jogo.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titulo} ({self.desenvolvedora})"

    def get_absolute_url(self):
        return reverse('games:detalhe', kwargs={'slug': self.slug})

    @property
    def get_capa(self):
        """Retorna o arquivo de upload ou a URL informada ou uma imagem padrão."""
        if self.imagem:
            return self.imagem.url
        if self.imagem_url:
            return self.imagem_url
        return "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80"

    @property
    def youtube_embed_id(self):
        """Extrai o ID do vídeo do YouTube para incorporação em iframe."""
        if not self.trailer_url:
            return None
        match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', self.trailer_url)
        return match.group(1) if match else None

    @property
    def media_avaliacoes(self):
        """Média das notas de 1 a 5 calculada via agregação."""
        resultado = self.avaliacoes.aggregate(media=Avg('nota'))['media']
        return round(resultado, 1) if resultado is not None else None

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()


class Avaliacao(models.Model):
    """
    Tabela 3: Avaliações dos jogos pelos usuários da comunidade.
    Relacionamento:
    - FK para Jogo
    - FK para User (Django auth.User)
    """
    NOTAS_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ (5) Excelente'),
        (4, '⭐⭐⭐⭐ (4) Muito Bom'),
        (3, '⭐⭐⭐ (3) Bom / Mediano'),
        (2, '⭐⭐ (2) Regular'),
        (1, '⭐ (1) Fraco / Ruim'),
    ]

    jogo = models.ForeignKey(
        Jogo,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name="Jogo Avaliado"
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='minhas_avaliacoes',
        verbose_name="Usuário Autor"
    )
    nota = models.PositiveSmallIntegerField(
        choices=NOTAS_CHOICES,
        default=5,
        verbose_name="Nota do Jogo"
    )
    titulo = models.CharField(max_length=120, verbose_name="Título da sua Análise")
    comentario = models.TextField(verbose_name="Comentário / Opinião Completa")
    recomenda = models.BooleanField(
        default=True,
        verbose_name="Você recomenda este jogo para outros jogadores?"
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name="Data da Avaliação")
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ['-criado_em']
        # Um usuário pode registrar uma avaliação por jogo (evita duplicatas e spam)
        unique_together = ('jogo', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} - {self.jogo.titulo} ({self.nota}/5)"
