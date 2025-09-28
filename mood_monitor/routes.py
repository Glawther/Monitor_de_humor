# mood_monitor/routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from datetime import date
from collections import Counter
import json
from flask_login import login_user, logout_user, login_required, current_user 

from . import db
from .models import MoodEntry, User, cores_humor, valor_humor_map, ordem_humor

main_bp = Blueprint('main', __name__)

# --- Funções Auxiliares (mantidas) ---
def calcular_media_movel(data_points, janela=3):
    """Calcula a média móvel simples sobre os pontos de dados."""
    if not data_points:
        return []
        
    tamanho = len(data_points)
    media_movel = []
    for i in range(tamanho):
        start_index = max(0, i - janela + 1)
        window = data_points[start_index:i+1]
        media = sum(window) / len(window)
        media_movel.append(round(media, 2))
    return media_movel
# ------------------------------------

# --- ROTAS DE AUTENTICAÇÃO ---

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuário ou senha inválidos')
            return redirect(url_for('main.login'))
        
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('login.html')

@main_bp.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.')
            return redirect(url_for('main.register'))

        user = User(username=username)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registro concluído! Você pode fazer login agora.')
        return redirect(url_for('main.login'))

    return render_template('register.html')


# --- ROTAS PRINCIPAIS PROTEGIDAS ---

@main_bp.route('/', methods=['GET', 'POST'])
@login_required 
def index():
    if request.method == 'POST':
        novo_humor = request.form.get('humor')
        data_registro = request.form.get('data')

        if novo_humor and data_registro:
            try:
                # CORREÇÃO CRÍTICA: Salva o user_id do usuário logado
                nova_entrada = MoodEntry(
                    humor=novo_humor, 
                    data=data_registro,
                    user_id=current_user.id 
                )
                db.session.add(nova_entrada)
                db.session.commit()
                
                return jsonify({'status': 'sucesso', 'mensagem': 'Humor registrado com sucesso!'})
                
            except Exception as e:
                db.session.rollback() 
                
                error_message = 'Erro interno ao salvar.'
                if 'IntegrityError' in str(e):
                    error_message = 'Erro ao registrar. Já existe um humor para esta data.'
                
                print(f"Erro ao salvar registro: {e}") 
                return jsonify({'status': 'erro', 'mensagem': error_message}), 400
        
        return jsonify({'status': 'erro', 'mensagem': 'Dados incompletos.'}), 400

    data_hoje = date.today().strftime('%Y-%m-%d')
    humores_json = json.dumps(ordem_humor)
    return render_template('index.html', data_padrao=data_hoje, humores_json=humores_json)


@main_bp.route('/dados_humor')
@login_required 
def dados_humor():
    # FILTRA: Apenas os registros do usuário atual
    historico_db = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.data).all()
    
    # === PONTO DE VERIFICAÇÃO DE DEBUG ===
    print(f"DEBUG: Registros encontrados para o usuário {current_user.id}: {historico_db}")
    # ======================================

    # 1. Dados para Gráfico de Linha
    humores_registrados = [registro.humor for registro in historico_db]
    labels = [registro.data for registro in historico_db]
    data_points = [valor_humor_map.get(humor, 0) for humor in humores_registrados] 
    background_colors = [cores_humor.get(humor, 'gray') for humor in humores_registrados]
    
    media_movel = calcular_media_movel(data_points, janela=3)

    # 2. Dados para Gráfico de Frequência (Barra/Pizza)
    contagem_humor = Counter(humores_registrados)
    frequencia_labels = ordem_humor
    frequencia_data = [contagem_humor.get(humor, 0) for humor in ordem_humor]
    frequencia_cores = [cores_humor.get(humor, 'gray') for humor in ordem_humor]

    # 3. Retorna TUDO em um único JSON
    return jsonify({
        'linha': {
            'labels': labels,
            'datasets': [
                {
                    'label': 'Nível de Humor Diário',
                    'data': data_points,
                    'backgroundColor': [c.replace('0.8', '0.4') for c in background_colors],
                    'borderColor': background_colors, 
                    'borderWidth': 2,
                    'pointRadius': 5,
                    'fill': False, 
                    'tension': 0.3,
                },
                {
                    'label': 'Média Móvel (3 dias)',
                    'data': media_movel,
                    'borderColor': 'rgb(255, 99, 132)',
                    'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                    'borderWidth': 3,
                    'pointRadius': 0,
                    'fill': False,
                    'tension': 0.3,
                }
            ]
        },
        'frequencia': {
            'labels': frequencia_labels,
            'data': frequencia_data,
            'backgroundColor': frequencia_cores
        }
    })