# wsgi.py
from app import create_app, db
import os

app = create_app()

# Opción 1: Solo en desarrollo
if os.environ.get('FLASK_ENV') == 'development':
    with app.app_context():
        db.create_all()

# Opción 2: Usar variable de entorno explícita
if os.environ.get('CREATE_TABLES', 'False').lower() == 'true':
    with app.app_context():
        db.create_all()

# Opción 3: Comando Flask personalizado (mejor práctica)
# En otro archivo: flask db_init
@app.cli.command('init-db')
def init_db():
    with app.app_context():
        db.create_all()
        print("Tablas creadas")

if __name__ == "__main__":
    app.run()
