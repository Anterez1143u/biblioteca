from flask_sqlalchemy import SQLAlchemy

# Instancia global de SQLAlchemy
db = SQLAlchemy()

# Función para inicializar datos de prueba
def inicializar_datos(app):
    with app.app_context():
        db.create_all()

        # Agregar usuarios de prueba si no existen
        from app import Usuario  # Importa el modelo Usuario aquí para evitar dependencias circulares

        if not Usuario.query.filter_by(email='admin@biblioteca.com').first():
            usuario_admin = Usuario(
                nombre='Admin',
                email='admin@biblioteca.com',
                telefono='123456789',
                rol='bibliotecario'
            )
            db.session.add(usuario_admin)
            print("Usuario admin creado.")

        if not Usuario.query.filter_by(email='lector@biblioteca.com').first():
            usuario_lector = Usuario(
                nombre='Lector',
                email='lector@biblioteca.com',
                telefono='987654321',
                rol='lector'
            )
            db.session.add(usuario_lector)
            print("Usuario lector creado.")

        db.session.commit()
