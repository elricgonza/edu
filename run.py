# run.py
from app import create_app, db

app = create_app()

def inicializar_si_necesario():
    with app.app_context():
        from app.models import Usr
        try:
            # Si no hay usuarios, inicializar
            if not Usr.query.first():
                import subprocess
                subprocess.run(['python', 'scripts/init_db.py'], check=True)
        except Exception as e:
            print(f"BD aún no disponible o ya inicializada: {e}")

inicializar_si_necesario()

if __name__ == '__main__':
    app.run(debug=False)
