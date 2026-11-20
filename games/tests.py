from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from games.models import Categoria, Jogo, Avaliacao


class GameHubTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Criação de usuários de teste
        self.user = User.objects.create_user(
            username='player_one',
            email='player1@gamehub.local',
            password='password123',
            first_name='Jogador 1'
        )
        self.other_user = User.objects.create_user(
            username='player_two',
            email='player2@gamehub.local',
            password='password123',
            first_name='Jogador 2'
        )

        # Criação de categoria (Tabela 1)
        self.categoria = Categoria.objects.create(
            nome='Aventura Épica',
            descricao='Jogos de aventura.',
            icone='bi-compass'
        )

        # Criação de jogo (Tabela 2, com FK para Categoria e FK para User)
        self.jogo = Jogo.objects.create(
            titulo='A Lenda do Dragão',
            categoria=self.categoria,
            criado_por=self.user,
            desenvolvedora='Dragon Studios',
            plataforma='PC, PS5',
            data_lancamento=date(2024, 1, 1),
            preco=149.90,
            descricao='Um jogo espetacular de RPG e dragões.'
        )

        # Criação de avaliação (Tabela 3, com FK para Jogo e FK para User)
        self.avaliacao = Avaliacao.objects.create(
            jogo=self.jogo,
            usuario=self.user,
            nota=5,
            titulo='Incrível!',
            comentario='Adorei os gráficos e a história envolvente.',
            recomenda=True
        )

    def test_relacionamento_entre_tabelas(self):
        """
        Requisito 1: Valida o relacionamento de pelo menos 3 tabelas com chave estrangeira.
        - Categoria -> Jogo (1:N)
        - User -> Jogo (1:N)
        - Jogo -> Avaliacao (1:N)
        - User -> Avaliacao (1:N)
        """
        # Verifica se o jogo está associado à categoria correta
        self.assertEqual(self.jogo.categoria.nome, 'Aventura Épica')
        self.assertIn(self.jogo, self.categoria.jogos.all())

        # Verifica se o jogo está associado ao usuário que o criou
        self.assertEqual(self.jogo.criado_por.username, 'player_one')
        self.assertIn(self.jogo, self.user.jogos_cadastrados.all())

        # Verifica a avaliação associada ao jogo e ao usuário
        self.assertEqual(self.avaliacao.jogo, self.jogo)
        self.assertEqual(self.avaliacao.usuario, self.user)
        self.assertIn(self.avaliacao, self.jogo.avaliacoes.all())

    def test_inscricao_de_usuario(self):
        """
        Requisito 2: 'O usuário deverá poder se inscrever no seu site.'
        """
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Crie sua Conta Gamer')

        # Testar envio do formulário de cadastro
        novo_usuario_dados = {
            'username': 'novogamer',
            'first_name': 'Carlos Silva',
            'email': 'carlos@gamehub.local',
            'password1': 'SenhaForte123!',
            'password2': 'SenhaForte123!',
        }
        post_response = self.client.post(reverse('cadastro'), data=novo_usuario_dados, follow=True)
        self.assertEqual(post_response.status_code, 200)
        self.assertTrue(User.objects.filter(username='novogamer').exists())

    def test_bloqueio_de_acoes_para_usuario_nao_logado(self):
        """
        Requisito 3: 'O usuário que não estiver logado não poderá fazer alguma, ou algumas, ações dentro do site.'
        - Não logado pode visualizar a home e detalhes do jogo
        - Não logado É REDIRECIONADO para o login se tentar cadastrar jogo
        - Não logado É REDIRECIONADO para o login se tentar avaliar jogo
        - Não logado É REDIRECIONADO para o login se tentar acessar meus jogos
        """
        # 1. Página inicial e detalhe são públicas (200 OK)
        resp_index = self.client.get(reverse('games:index'))
        self.assertEqual(resp_index.status_code, 200)

        resp_detalhe = self.client.get(reverse('games:detalhe', kwargs={'slug': self.jogo.slug}))
        self.assertEqual(resp_detalhe.status_code, 200)
        # Deve exibir aviso de bloqueio na página de detalhes para deslogados
        self.assertContains(resp_detalhe, 'Quer avaliar este jogo?')

        # 2. Tentativa de cadastrar jogo sem estar logado -> Redireciona para login (302)
        resp_cadastrar = self.client.get(reverse('games:cadastrar_jogo'))
        self.assertEqual(resp_cadastrar.status_code, 302)
        self.assertIn(reverse('login'), resp_cadastrar.url)

        # 3. Tentativa de avaliar jogo sem estar logado -> Redireciona para login (302)
        resp_avaliar = self.client.post(
            reverse('games:adicionar_avaliacao', kwargs={'slug': self.jogo.slug}),
            data={'nota': 4, 'titulo': 'Muito bom', 'comentario': 'Gostei bastante.', 'recomenda': True}
        )
        self.assertEqual(resp_avaliar.status_code, 302)
        self.assertIn(reverse('login'), resp_avaliar.url)

        # 4. Tentativa de acessar 'meus-jogos' sem estar logado -> Redireciona para login (302)
        resp_meus_jogos = self.client.get(reverse('games:meus_jogos'))
        self.assertEqual(resp_meus_jogos.status_code, 302)
        self.assertIn(reverse('login'), resp_meus_jogos.url)

    def test_usuario_logado_consegue_executar_acoes(self):
        """
        Verifica que um usuário logado pode cadastrar jogos e avaliar,
        e que o botão 'Divulgar Jogo' é removido da barra superior (navbar).
        """
        self.client.login(username='player_two', password='password123')

        # Verifica que o link 'Divulgar Jogo' foi removido da barra superior para usuário logado,
        # mas o botão de ação rápida 'Novo Jogo' continua disponível para ele
        resp_home = self.client.get(reverse('games:index'))
        self.assertNotContains(resp_home, '<span>Divulgar Jogo</span>')
        self.assertContains(resp_home, 'Novo Jogo')

        # Consegue acessar a página de cadastro de jogo
        resp_cadastrar = self.client.get(reverse('games:cadastrar_jogo'))
        self.assertEqual(resp_cadastrar.status_code, 200)
        self.assertContains(resp_cadastrar, 'Divulgar Novo Jogo')

        # Cadastra um novo jogo com sucesso
        dados_jogo = {
            'titulo': 'Jogo do Jogador Dois',
            'categoria': self.categoria.id,
            'desenvolvedora': 'Indie Studio',
            'distribuidora': 'Indie Pub',
            'plataforma': 'PC',
            'data_lancamento': '2024-05-10',
            'preco': '0.00',
            'descricao': 'Um jogo muito divertido para testar o cadastro.',
        }
        resp_post = self.client.post(reverse('games:cadastrar_jogo'), data=dados_jogo, follow=True)
        self.assertEqual(resp_post.status_code, 200)
        self.assertTrue(Jogo.objects.filter(titulo='Jogo do Jogador Dois').exists())

        # Consegue avaliar o jogo
        dados_avaliacao = {
            'nota': 4,
            'titulo': 'Ótimo jogo',
            'comentario': 'Divertido e desafiador.',
            'recomenda': True
        }
        resp_av = self.client.post(
            reverse('games:adicionar_avaliacao', kwargs={'slug': self.jogo.slug}),
            data=dados_avaliacao,
            follow=True
        )
        self.assertEqual(resp_av.status_code, 200)
        self.assertTrue(Avaliacao.objects.filter(jogo=self.jogo, usuario=self.other_user).exists())
