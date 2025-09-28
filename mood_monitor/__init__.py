# mood_monitor/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_migrate import Migrate # NOVO: Importa a extensão de migração

# Inicializa as extensões fora da factory
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate() # NOVO: Inicializa a extensão Migrate

def create_app():
    """Cria e configura a instância da aplicação Flask."""
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura' 
    app.config.from_object('config.Config')

    # Inicializa as extensões com a app
    db.init_app(app)
    login_manager.init_app(app)
    
    # NOVO: Inicializa o Flask-Migrate, ligando-o ao app e db
    migrate.init_app(app, db) 
    
    login_manager.login_view = 'main.login' 

    # Implementa a função de carregamento de usuário
    from .models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Importa os modelos para que o db.create_all() os encontre
    from . import models
    
    # --- Blueprints ---
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app