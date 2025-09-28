# run.py

from mood_monitor import create_app, db

# Cria a aplicação. O Flask-Migrate vai detectar isso automaticamente.
app = create_app()

if __name__ == '__main__':
    # REMOVIDO: Removemos o db.create_all() daqui, pois as migrações assumirão a criação.
    # No entanto, vamos deixá-lo aqui DESCOMENTADO pela primeira execução, 
    # para garantir que o arquivo .db exista e que o Alembic possa inicializá-lo.
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)