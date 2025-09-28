# mood_monitor/models.py

from . import db
from flask_login import UserMixin # NOVO: Para usar na classe User
from werkzeug.security import generate_password_hash, check_password_hash # NOVO: Para hashing de senha

# --- MODELO DE DADOS (User) ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Funções para manipulação segura de senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- MODELO DE DADOS (MoodEntry) ---
class MoodEntry(db.Model):
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    humor = db.Column(db.String(10), nullable=False)
    data = db.Column(db.String(10), unique=True, nullable=False) 
    
    # NOVO: Chave estrangeira para ligar o registro de humor ao usuário
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 

    def __repr__(self):
        return f'<MoodEntry {self.data}: {self.humor}>'
        
# --- Mapeamento de Cores e Valores ---
cores_humor = {
    'Ótimo': 'rgba(75, 192, 192, 0.8)',
    'Bom': 'rgba(153, 102, 255, 0.8)',
    'Neutro': 'rgba(255, 205, 86, 0.8)',
    'Ruim': 'rgba(255, 159, 64, 0.8)',
    'Péssimo': 'rgba(255, 99, 132, 0.8)'
}
valor_humor_map = {
    'Péssimo': 1,
    'Ruim': 2,
    'Neutro': 3,
    'Bom': 4,
    'Ótimo': 5
}
ordem_humor = ['Péssimo', 'Ruim', 'Neutro', 'Bom', 'Ótimo']