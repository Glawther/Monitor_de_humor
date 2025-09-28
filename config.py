# config.py

class Config:
    """Configurações de base para a aplicação."""
    # Configuração do Banco de Dados SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mood_monitor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False