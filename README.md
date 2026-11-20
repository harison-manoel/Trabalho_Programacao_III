# GameHub - Portal de Divulgação e Avaliação de Jogos

## Discente:
Harison Manoel dos Santos Matos.
## Turma:
4º período de ADS de 2026.
## Link para o projeto no PythonAnywhere: 
(Adicione aqui o link gerado após o deploy, ex: https://SEU_USUARIO.pythonanywhere.com/)
## Link para o vídeo de apresentação do projeto:




# Outras informações:


## Como Executar o Projeto Localmente

### 1. Criar o Ambiente Virtual (venv)
No terminal, dentro da pasta raiz do projeto, execute:
```bash
python -m venv .venv
```

### 2. Ativar o Ambiente Virtual
* **No Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Caso ocorra erro de execução de scripts no PowerShell, execute antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

### 3. Instalar as Dependências do Projeto
Com o ambiente virtual ativado, instale os pacotes listados no `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Executar as Migrações do Banco de Dados
Crie as tabelas necessárias no banco SQLite local:
```bash
python manage.py migrate
```

### 5. Povoar o Banco de Dados com Dados de Exemplo (Opcional, mas Recomendado)
Para carregar as categorias, jogos populares com sinopses e trailers, avaliações comunitárias e contas de teste prontas para uso:
```bash
python seed_data.py
```

### 6. Iniciar o Servidor de Desenvolvimento
```bash
python manage.py runserver
```
Acesse a aplicação no navegador em: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

### 7. Executar os Testes Automatizados (Opcional)
Para validar os relacionamentos entre modelos, controle de permissões e cadastro de usuários:
```bash
python manage.py test
```



##  Credenciais Pré-configuradas para Testes (seed_data.py)

| Perfil | Usuário | Senha | Descrição |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` | `admin123` | Acesso total ao painel administrativo `/admin/` e gestão geral |
| **Usuário Gamer 1** | `lucas_gamer` | `gamer123` | Usuário comum com jogos cadastrados para teste de edição/exclusão |
| **Usuário Gamer 2** | `paula_rpg` | `gamer123` | Usuária comum para testar avaliações colaborativas |
