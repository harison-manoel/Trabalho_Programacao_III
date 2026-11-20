import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()

from django.contrib.auth.models import User
from games.models import Categoria, Jogo, Avaliacao

def seed():
    print("Iniciando povoamento de dados de exemplo...")

    # 1. Criar Superusuário e Usuário Padrão
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@gamehub.local',
            'first_name': 'Administrador',
            'last_name': 'GameHub',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("-> Superusuário 'admin' criado com sucesso (senha: admin123).")
    else:
        print("-> Superusuário 'admin' já existe.")

    gamer_user, created = User.objects.get_or_create(
        username='lucas_gamer',
        defaults={
            'email': 'lucas@exemplo.com',
            'first_name': 'Lucas',
            'last_name': 'Pereira',
        }
    )
    if created:
        gamer_user.set_password('gamer123')
        gamer_user.save()
        print("-> Usuário comum 'lucas_gamer' criado (senha: gamer123).")
    else:
        print("-> Usuário 'lucas_gamer' já existe.")

    paula_user, created = User.objects.get_or_create(
        username='paula_rpg',
        defaults={
            'email': 'paula@exemplo.com',
            'first_name': 'Paula',
            'last_name': 'Souza',
        }
    )
    if created:
        paula_user.set_password('gamer123')
        paula_user.save()
        print("-> Usuária comum 'paula_rpg' criada (senha: gamer123).")

    # 2. Criar Categorias
    categorias_data = [
        ('RPG', 'Jogos de interpretação de papéis com foco em progressão, histórias profundas e escolhas.', 'bi-shield-shaded'),
        ('Ação & Aventura', 'Títulos dinâmicos com combate, exploração de mundos e narrativas cinematográficas.', 'bi-fire'),
        ('Indie', 'Produções independentes inovadoras com arte única e jogabilidade autêntica.', 'bi-gem'),
        ('Estratégia', 'Jogos que exigem planejamento tático, raciocínio lógico e gestão de recursos.', 'bi-diagram-3-fill'),
        ('FPS & Tiro', 'Tiros em primeira ou terceira pessoa com ação tática e alta precisão.', 'bi-crosshair'),
        ('Terror & Sobrevivência', 'Experiências imersivas de suspense, horror psicológico e gerenciamento escasso.', 'bi-radioactive'),
    ]

    categorias_dict = {}
    for nome, desc, icone in categorias_data:
        cat, _ = Categoria.objects.get_or_create(
            nome=nome,
            defaults={'descricao': desc, 'icone': icone}
        )
        categorias_dict[nome] = cat
    print(f"-> {len(categorias_dict)} categorias configuradas.")

    # 3. Criar Jogos
    jogos_data = [
        {
            'titulo': 'The Witcher 3: Wild Hunt',
            'categoria': categorias_dict['RPG'],
            'criado_por': admin_user,
            'desenvolvedora': 'CD Projekt Red',
            'distribuidora': 'CD Projekt',
            'plataforma': 'PC, PlayStation 5, Xbox Series X/S, Switch',
            'data_lancamento': date(2015, 5, 19),
            'preco': 129.90,
            'imagem_url': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=c0i88t0Kacs',
            'site_oficial': 'https://www.thewitcher.com/witcher3',
            'destaque': True,
            'descricao': (
                "The Witcher 3: Wild Hunt é um RPG de ação em mundo aberto focado em narrativa. "
                "Você joga como Geralt de Rívia, um mercenário caçador de monstros em busca de Ciri, "
                "a Criança da Profecia. Em um continente devastado pela guerra e repleto de aberrações, "
                "cada escolha carrega consequências morais imprevisíveis em um dos universos mais detalhados "
                "já criados nos videogames."
            )
        },
        {
            'titulo': 'Elden Ring',
            'categoria': categorias_dict['RPG'],
            'criado_por': gamer_user,
            'desenvolvedora': 'FromSoftware',
            'distribuidora': 'Bandai Namco Entertainment',
            'plataforma': 'PC, PlayStation 5, Xbox Series X/S',
            'data_lancamento': date(2022, 2, 25),
            'preco': 229.90,
            'imagem_url': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=E3Huy2cdih0',
            'site_oficial': 'https://en.bandainamcoent.eu/elden-ring/elden-ring',
            'destaque': True,
            'descricao': (
                "O Novo RPG de Ação e Fantasia desenvolvido pela FromSoftware e escrito por Hidetaka Miyazaki "
                "com a colaboração de George R. R. Martin. Levante-se, Maculado, e seja guiado pela graça para "
                "portar o poder do Anel Prístino e se tornar um Lorde Prístino nas Terras Intermédias. Um mundo vasto, "
                "masmorras interconectadas e combate desafiador impecável."
            )
        },
        {
            'titulo': 'Hollow Knight',
            'categoria': categorias_dict['Indie'],
            'criado_por': paula_user,
            'desenvolvedora': 'Team Cherry',
            'distribuidora': 'Team Cherry',
            'plataforma': 'PC, Nintendo Switch, PlayStation 4, Xbox One',
            'data_lancamento': date(2017, 2, 24),
            'preco': 46.99,
            'imagem_url': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=UAO2urG23S4',
            'site_oficial': 'https://www.hollowknight.com/',
            'destaque': True,
            'descricao': (
                "Forje seu próprio caminho em Hollow Knight! Uma clássica aventura 2D em estilo metroidvania "
                "em um vasto reino subterrâneo de insetos e heróis em ruínas chamado Hallownest. Explore cavernas "
                "sinuosas, lute contra criaturas corrompidas e faça amizade com insetos bizarros em uma obra-prima de "
                "design, combate preciso e trilha sonora inesquecível."
            )
        },
        {
            'titulo': 'Cyberpunk 2077',
            'categoria': categorias_dict['Ação & Aventura'],
            'criado_por': gamer_user,
            'desenvolvedora': 'CD Projekt Red',
            'distribuidora': 'CD Projekt',
            'plataforma': 'PC, PlayStation 5, Xbox Series X/S',
            'data_lancamento': date(2020, 12, 10),
            'preco': 199.90,
            'imagem_url': 'https://images.unsplash.com/photo-1578632767115-351597cf2477?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=qIcTM8WXFjk',
            'site_oficial': 'https://www.cyberpunk.net/',
            'destaque': False,
            'descricao': (
                "Cyberpunk 2077 é um RPG de ação e aventura em mundo aberto ambientado na megalópole futurista "
                "de Night City, obcecada por poder, glamour e modificações corporais. Você joga como V, um mercenário "
                "cyberpunk em busca de um implante único que carrega a chave para a imortalidade."
            )
        },
        {
            'titulo': 'Counter-Strike 2',
            'categoria': categorias_dict['FPS & Tiro'],
            'criado_por': admin_user,
            'desenvolvedora': 'Valve Corporation',
            'distribuidora': 'Valve',
            'plataforma': 'PC (Steam)',
            'data_lancamento': date(2023, 9, 27),
            'preco': 0.00,
            'imagem_url': 'https://images.unsplash.com/photo-1542751110-97427bbecf20?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=nSE38VJhy44',
            'site_oficial': 'https://store.steampowered.com/app/730/CounterStrike_2/',
            'destaque': False,
            'descricao': (
                "Por mais de duas décadas, o Counter-Strike ofereceu uma experiência competitiva de elite "
                "moldada por milhões de jogadores em todo o mundo. Agora, o próximo capítulo começa com "
                "Counter-Strike 2. O maior salto técnico na história do CS, trazendo nova física para fumaças volumétricas, "
                "taxas de tique sub-tick e mapas totalmente reformulados na engine Source 2. Gratuito para jogar!"
            )
        },
        {
            'titulo': 'Baldur\'s Gate 3',
            'categoria': categorias_dict['RPG'],
            'criado_por': paula_user,
            'desenvolvedora': 'Larian Studios',
            'distribuidora': 'Larian Studios',
            'plataforma': 'PC, PlayStation 5, Xbox Series X/S',
            'data_lancamento': date(2023, 8, 3),
            'preco': 199.99,
            'imagem_url': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?auto=format&fit=crop&w=800&q=80',
            'trailer_url': 'https://www.youtube.com/watch?v=1T22wNlUiNh',
            'site_oficial': 'https://baldursgate3.game/',
            'destaque': True,
            'descricao': (
                "Vencedor do prêmio de Jogo do Ano (GOTY), Baldur's Gate 3 é um RPG cinematográfico de última geração "
                "ambientado no universo de Dungeons & Dragons. Reúna seu grupo e retorne aos Reinos Esquecidos em uma história "
                "de companheirismo e traição, sacrifício e sobrevivência, e a atração pelo poder absoluto."
            )
        }
    ]

    jogos_dict = {}
    for j_data in jogos_data:
        jogo, _ = Jogo.objects.get_or_create(
            titulo=j_data['titulo'],
            defaults=j_data
        )
        jogos_dict[jogo.titulo] = jogo
    print(f"-> {len(jogos_dict)} jogos cadastrados.")

    # 4. Criar Avaliações
    avaliacoes_data = [
        {
            'jogo': jogos_dict['The Witcher 3: Wild Hunt'],
            'usuario': gamer_user,
            'nota': 5,
            'titulo': 'Uma obra-prima incontestável!',
            'comentario': 'História espetacular, trilha sonora emocionante e missões secundárias que parecem campanhas inteiras. Um dos melhores RPGs já feitos.',
            'recomenda': True
        },
        {
            'jogo': jogos_dict['The Witcher 3: Wild Hunt'],
            'usuario': paula_user,
            'nota': 5,
            'titulo': 'Geralt é lendário',
            'comentario': 'As expansões Hearts of Stone e Blood and Wine são tão boas quanto o jogo principal. Simplesmente obrigatório para quem gosta de fantasia.',
            'recomenda': True
        },
        {
            'jogo': jogos_dict['Elden Ring'],
            'usuario': paula_user,
            'nota': 5,
            'titulo': 'Mundo aberto perfeito e combate viciante',
            'comentario': 'A sensação de explorar cada canto do mapa sem saber o que vai encontrar é única. Difícil, mas extremamente recompensador.',
            'recomenda': True
        },
        {
            'jogo': jogos_dict['Hollow Knight'],
            'usuario': gamer_user,
            'nota': 5,
            'titulo': 'O auge dos jogos Indie',
            'comentario': 'Direção de arte sublime, chefes desafiadores e controles extremamente responsivos. Vale cada centavo e muito mais.',
            'recomenda': True
        },
        {
            'jogo': jogos_dict['Counter-Strike 2'],
            'usuario': gamer_user,
            'nota': 4,
            'titulo': 'Muito bom, mas precisa de ajustes no matchmaking',
            'comentario': 'A fumaça responsiva é revolucionária e os gráficos ficaram lindos. A Valve só precisa melhorar o sistema anti-cheat.',
            'recomenda': True
        },
    ]

    for av_data in avaliacoes_data:
        Avaliacao.objects.get_or_create(
            jogo=av_data['jogo'],
            usuario=av_data['usuario'],
            defaults=av_data
        )
    print(f"-> {len(avaliacoes_data)} avaliações cadastradas.")
    print("\n✅ Povoamento concluído com sucesso!")

if __name__ == '__main__':
    seed()
