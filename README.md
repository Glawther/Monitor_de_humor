# Monitor de Humor Diário (Python/Flask)

Este é um projeto full-stack leve, construído com Python (Flask) no backend e Chart.js no frontend, para registrar e visualizar o humor diário. O projeto utiliza o padrão Factory e Blueprints, com autenticação (Flask-Login) e persistência de dados (Flask-SQLAlchemy).

## 🚀 Tecnologias Utilizadas

- **Backend:** Python 3.x, Flask
- **Banco de Dados:** SQLite (Flask-SQLAlchemy)
- **Extensões:** Flask-Login (Autenticação), Flask-Migrate (Migrações de DB)
- **Frontend:** HTML/CSS/JavaScript, Chart.js (Visualização de Dados)
- **Gerenciamento de Dependências:** Pipenv

## ⚙️ Instalação e Execução

Siga os passos abaixo para configurar e rodar o projeto localmente.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seuusuario/monitor-de-humor.git](https://github.com/seuusuario/monitor-de-humor.git)
cd monitor-de-humor

### 2. Configurar Ambiente com Pipenv
Este projeto usa o Pipenv para gerenciamento de dependências.

Bash

# 1. Instala o Pipenv e cria o ambiente virtual (pode demorar)
pipenv install

# 2. Ativa o ambiente virtual (o shell do terminal mudará)
pipenv shell

3. Define a variável FLASK_APP para o Flask encontrar a aplicação modularizada
$env:FLASK_APP="mood_monitor"
### 3. Configurar o Banco de Dados
Crie as tabelas e a estrutura do banco de dados usando o Flask-Migrate:

Bash

# Inicializa o repositório de migrações (se for a primeira vez)
flask db init 

# Aplica a migração inicial para criar as tabelas (User e MoodEntry)
flask db upgrade
### 4. Rodar a Aplicação
Inicie o servidor de desenvolvimento do Flask:

Bash

python run.py
Acesse http://127.0.0.1:5000/ no seu navegador.

### 5. Primeiro Acesso
Ao acessar a URL, você será redirecionado para a tela de login.

Clique em "Registrar" para criar seu primeiro usuário.

Faça login.

Comece a registrar seu humor e veja os gráficos se atualizarem via AJAX.