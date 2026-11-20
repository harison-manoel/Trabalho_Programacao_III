from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator

from .models import Categoria, Jogo, Avaliacao
from .forms import JogoForm, AvaliacaoForm, UsuarioCadastroForm


def index(request):
    """
    Página inicial pública:
    Apresenta banner de destaque, estatísticas, filtros por categoria,
    busca por termo, ordenação e listagem paginada de jogos.
    """
    busca = request.GET.get('busca', '').strip()
    categoria_slug = request.GET.get('categoria', '').strip()
    ordem = request.GET.get('ordem', 'novos')

    jogos = Jogo.objects.select_related('categoria', 'criado_por').annotate(
        nota_media=Avg('avaliacoes__nota'),
        num_avaliacoes=Count('avaliacoes')
    )

    # Filtro por texto (título, descrição, desenvolvedora, distribuidora)
    if busca:
        jogos = jogos.filter(
            Q(titulo__icontains=busca) |
            Q(descricao__icontains=busca) |
            Q(desenvolvedora__icontains=busca) |
            Q(plataforma__icontains=busca)
        )

    # Filtro por categoria
    categoria_selecionada = None
    if categoria_slug:
        categoria_selecionada = get_object_or_404(Categoria, slug=categoria_slug)
        jogos = jogos.filter(categoria=categoria_selecionada)

    # Ordenação
    if ordem == 'nota':
        jogos = jogos.order_by('-nota_media', '-num_avaliacoes', '-criado_em')
    elif ordem == 'preco_menor':
        jogos = jogos.order_by('preco', '-criado_em')
    elif ordem == 'preco_maior':
        jogos = jogos.order_by('-preco', '-criado_em')
    elif ordem == 'antigos':
        jogos = jogos.order_by('data_lancamento')
    else:  # 'novos' default
        jogos = jogos.order_by('-criado_em')

    # Paginação: 6 jogos por página para layout em grade
    paginator = Paginator(jogos, 6)
    page_number = request.GET.get('page')
    jogos_paginados = paginator.get_page(page_number)

    # Categorias com contagem de jogos
    categorias = Categoria.objects.annotate(total=Count('jogos')).order_by('nome')

    # Jogos em destaque (para carrossel/hero)
    jogos_destaque = Jogo.objects.filter(destaque=True).select_related('categoria')[:4]

    # Estatísticas globais do portal
    estatisticas = {
        'total_jogos': Jogo.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_avaliacoes': Avaliacao.objects.count(),
        'total_usuarios': User.objects.count(),
    }

    context = {
        'jogos': jogos_paginados,
        'categorias': categorias,
        'categoria_selecionada': categoria_selecionada,
        'jogos_destaque': jogos_destaque,
        'estatisticas': estatisticas,
        'busca': busca,
        'ordem': ordem,
    }
    return render(request, 'games/index.html', context)


def detalhe_jogo(request, slug):
    """
    Página pública de detalhes de um jogo:
    Mostra informações completas, capas, trailer, plataformas e análises da comunidade.
    Se o usuário estiver autenticado, disponibiliza o formulário para avaliar.
    Se não estiver autenticado, bloqueia o envio e sugere login/cadastro.
    """
    jogo = get_object_or_404(
        Jogo.objects.select_related('categoria', 'criado_por'),
        slug=slug
    )
    avaliacoes = jogo.avaliacoes.select_related('usuario').order_by('-criado_em')

    # Avaliação prévia do usuário atual se estiver logado
    minha_avaliacao = None
    form_avaliacao = None

    if request.user.is_authenticated:
        minha_avaliacao = avaliacoes.filter(usuario=request.user).first()
        if minha_avaliacao:
            form_avaliacao = AvaliacaoForm(instance=minha_avaliacao)
        else:
            form_avaliacao = AvaliacaoForm()

    context = {
        'jogo': jogo,
        'avaliacoes': avaliacoes,
        'minha_avaliacao': minha_avaliacao,
        'form_avaliacao': form_avaliacao,
    }
    return render(request, 'games/detalhe.html', context)


# =====================================================================
# AÇÕES PROTEGIDAS (Exigem usuário autenticado / logado)
# Atende ao Requisito 3: "O usuário que não estiver 'logado' não poderá
# fazer alguma, ou algumas, ações dentro do site."
# =====================================================================

@login_required(login_url='login')
def cadastrar_jogo(request):
    """
    AÇÃO PROTEGIDA: Cadastrar um novo jogo no portal.
    Apenas usuários logados podem acessar.
    """
    if request.method == 'POST':
        form = JogoForm(request.POST, request.FILES)
        if form.is_valid():
            jogo = form.save(commit=False)
            jogo.criado_por = request.user
            jogo.save()
            messages.success(request, f'🎮 Jogo "{jogo.titulo}" cadastrado com sucesso!')
            return redirect('games:detalhe', slug=jogo.slug)
    else:
        form = JogoForm()

    context = {
        'form': form,
        'titulo_pagina': 'Divulgar Novo Jogo',
        'botao_texto': 'Publicar Jogo'
    }
    return render(request, 'games/jogo_form.html', context)


@login_required(login_url='login')
def editar_jogo(request, slug):
    """
    AÇÃO PROTEGIDA: Editar informações de um jogo.
    Permitido apenas ao autor original do cadastro ou administradores.
    """
    jogo = get_object_or_404(Jogo, slug=slug)

    # Verificação de permissão: apenas o criador ou staff pode editar
    if jogo.criado_por != request.user and not request.user.is_staff:
        messages.error(request, '⛔ Você não tem permissão para editar este jogo, pois não foi cadastrado por você.')
        return redirect('games:detalhe', slug=jogo.slug)

    if request.method == 'POST':
        form = JogoForm(request.POST, request.FILES, instance=jogo)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ As informações de "{jogo.titulo}" foram atualizadas com sucesso!')
            return redirect('games:detalhe', slug=jogo.slug)
    else:
        form = JogoForm(instance=jogo)

    context = {
        'form': form,
        'jogo': jogo,
        'titulo_pagina': f'Editar Jogo: {jogo.titulo}',
        'botao_texto': 'Salvar Alterações'
    }
    return render(request, 'games/jogo_form.html', context)


@login_required(login_url='login')
def deletar_jogo(request, slug):
    """
    AÇÃO PROTEGIDA: Excluir um jogo divulgado.
    Permitido apenas ao autor original do cadastro ou administradores.
    """
    jogo = get_object_or_404(Jogo, slug=slug)

    if jogo.criado_por != request.user and not request.user.is_staff:
        messages.error(request, '⛔ Você não tem permissão para excluir este jogo.')
        return redirect('games:detalhe', slug=jogo.slug)

    if request.method == 'POST':
        titulo = jogo.titulo
        jogo.delete()
        messages.success(request, f'🗑️ O jogo "{titulo}" foi removido com sucesso.')
        return redirect('games:index')

    return render(request, 'games/jogo_confirm_delete.html', {'jogo': jogo})


@login_required(login_url='login')
def meus_jogos(request):
    """
    AÇÃO PROTEGIDA: Painel onde o usuário visualiza e gerencia
    todos os jogos que ele próprio cadastrou no portal.
    """
    jogos = Jogo.objects.filter(criado_por=request.user).select_related('categoria').annotate(
        nota_media=Avg('avaliacoes__nota'),
        num_avaliacoes=Count('avaliacoes')
    ).order_by('-criado_em')

    context = {
        'jogos': jogos,
        'total': jogos.count(),
    }
    return render(request, 'games/meus_jogos.html', context)


@login_required(login_url='login')
def adicionar_avaliacao(request, slug):
    """
    AÇÃO PROTEGIDA: Enviar avaliação para um jogo.
    Se o usuário não estiver logado, é redirecionado para a tela de login.
    Atualiza a avaliação caso já exista ou cria uma nova.
    """
    jogo = get_object_or_404(Jogo, slug=slug)

    if request.method == 'POST':
        avaliacao_existente = Avaliacao.objects.filter(jogo=jogo, usuario=request.user).first()

        if avaliacao_existente:
            form = AvaliacaoForm(request.POST, instance=avaliacao_existente)
            acao = "atualizada"
        else:
            form = AvaliacaoForm(request.POST)
            acao = "publicada"

        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.jogo = jogo
            avaliacao.usuario = request.user
            avaliacao.save()
            messages.success(request, f'⭐ Sua avaliação para "{jogo.titulo}" foi {acao} com sucesso!')
        else:
            messages.error(request, '⚠️ Verifique os erros no formulário de avaliação.')

    return redirect('games:detalhe', slug=jogo.slug)


@login_required(login_url='login')
def deletar_avaliacao(request, id):
    """
    AÇÃO PROTEGIDA: Remover a avaliação deixada pelo usuário.
    """
    avaliacao = get_object_or_404(Avaliacao, id=id)

    if avaliacao.usuario != request.user and not request.user.is_staff:
        messages.error(request, '⛔ Você não tem permissão para excluir esta avaliação.')
        return redirect('games:detalhe', slug=avaliacao.jogo.slug)

    slug_jogo = avaliacao.jogo.slug
    avaliacao.delete()
    messages.success(request, '🗑️ Sua avaliação foi excluída.')
    return redirect('games:detalhe', slug=slug_jogo)


# =====================================================================
# AUTENTICAÇÃO E INSCRIÇÃO DE USUÁRIOS
# Atende ao Requisito 2: "O usuário deverá poder se inscrever no seu site."
# =====================================================================

def cadastrar_usuario(request):
    """
    Inscrição / Registro de novo usuário no site.
    Após cadastro com sucesso, efetua login automático e redireciona.
    """
    if request.user.is_authenticated:
        return redirect('games:index')

    if request.method == 'POST':
        form = UsuarioCadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(
                request,
                f'🎉 Bem-vindo ao GameHub, {user.first_name or user.username}! Sua conta foi criada com sucesso.'
            )
            return redirect('games:index')
    else:
        form = UsuarioCadastroForm()

    return render(request, 'registration/cadastro.html', {'form': form})


def login_view(request):
    """
    Página de login personalizada integrada com o design gamer do portal.
    """
    if request.user.is_authenticated:
        return redirect('games:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'🎮 Bem-vindo de volta, {user.first_name or user.username}!')
            next_url = request.GET.get('next') or 'games:index'
            return redirect(next_url)
        else:
            messages.error(request, '❌ Nome de usuário ou senha incorretos.')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """
    Encerra a sessão do usuário e redireciona para a página inicial com mensagem.
    """
    if request.user.is_authenticated:
        auth_logout(request)
        messages.info(request, '👋 Você encerrou sua sessão com sucesso. Até logo!')
    return redirect('games:index')
