from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inicializa Flask-Migrate
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

# MODELOS
class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    nacionalidad = db.Column(db.String(50))
    libros = db.relationship('Libro', backref='autor', lazy=True)

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    anio_publicacion = db.Column(db.Integer)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'), nullable=False)
    prestamos = db.relationship('Prestamo', backref='libro', lazy=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    rol = db.Column(db.String(20))  # lector o bibliotecario
    prestamos = db.relationship('Prestamo', backref='usuario', lazy=True)

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fecha_prestamo = db.Column(db.Date)
    fecha_devolucion = db.Column(db.Date)
    devuelto = db.Column(db.Boolean, default=False)

# RUTAS LIBROS
@app.route('/')
@app.route('/libros')
def listar_libros():
    libros = Libro.query.all()
    return render_template('libros.html', libros=libros)

@app.route('/libros/crear', methods=['GET', 'POST'])
def crear_libro():
    if request.method == 'POST':
        libro = Libro(
            titulo=request.form['titulo'],
            genero=request.form['genero'],
            anio_publicacion=request.form['anio_publicacion'],
            autor_id=request.form['autor_id']
        )
        db.session.add(libro)
        db.session.commit()
        return redirect(url_for('listar_libros'))
    autores = Autor.query.all()
    return render_template('crear_libro.html', autores=autores)

@app.route('/libros/editar/<int:libro_id>', methods=['GET', 'POST'])
def editar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.genero = request.form['genero']
        libro.anio_publicacion = request.form['anio_publicacion']
        libro.autor_id = request.form['autor_id']
        db.session.commit()
        return redirect(url_for('listar_libros'))
    autores = Autor.query.all()
    return render_template('editar_libro.html', libro=libro, autores=autores)

@app.route('/libros/eliminar/<int:libro_id>')
def eliminar_libro(libro_id):
    libro = Libro.query.get_or_404(libro_id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('listar_libros'))

# RUTAS AUTORES
@app.route('/autores')
def listar_autores():
    autores = Autor.query.all()
    return render_template('autores.html', autores=autores)

@app.route('/autores/crear', methods=['GET', 'POST'])
def crear_autor():
    if request.method == 'POST':
        autor = Autor(nombre=request.form['nombre'], nacionalidad=request.form['nacionalidad'])
        db.session.add(autor)
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('crear_autor.html')

@app.route('/autores/editar/<int:autor_id>', methods=['GET', 'POST'])
def editar_autor(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    if request.method == 'POST':
        autor.nombre = request.form['nombre']
        autor.nacionalidad = request.form['nacionalidad']
        db.session.commit()
        return redirect(url_for('listar_autores'))
    return render_template('editar_autor.html', autor=autor)

@app.route('/autores/eliminar/<int:autor_id>')
def eliminar_autor(autor_id):
    autor = Autor.query.get_or_404(autor_id)
    db.session.delete(autor)
    db.session.commit()
    return redirect(url_for('listar_autores'))

# RUTAS USUARIOS
@app.route('/usuarios')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        usuario = Usuario(
            nombre=request.form['nombre'],
            email=request.form['email'],
            telefono=request.form['telefono'],
            rol=request.form['rol']
        )
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('crear_usuario.html')

@app.route('/usuarios/editar/<int:usuario_id>', methods=['GET', 'POST'])
def editar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        usuario.telefono = request.form['telefono']
        usuario.rol = request.form['rol']
        db.session.commit()
        return redirect(url_for('listar_usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/eliminar/<int:usuario_id>')
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('listar_usuarios'))

# RUTAS PRÉSTAMOS
@app.route('/prestamos')
def listar_prestamos():
    prestamos = Prestamo.query.all()
    return render_template('prestamos.html', prestamos=prestamos)

@app.route('/prestamos/crear', methods=['GET', 'POST'])
def crear_prestamo():
    if request.method == 'POST':
        prestamo = Prestamo(
            libro_id=request.form['libro_id'],
            usuario_id=request.form['usuario_id'],
            fecha_prestamo=request.form['fecha_prestamo'],
            fecha_devolucion=request.form['fecha_devolucion']
        )
        db.session.add(prestamo)
        db.session.commit()
        return redirect(url_for('listar_prestamos'))
    libros = Libro.query.all()
    usuarios = Usuario.query.all()
    return render_template('crear_prestamo.html', libros=libros, usuarios=usuarios)

@app.route('/prestamos/devolver/<int:prestamo_id>')
def marcar_devueltos(prestamo_id):
    prestamo = Prestamo.query.get_or_404(prestamo_id)
    prestamo.devuelto = True
    db.session.commit()
    return redirect(url_for('listar_prestamos'))

# CONSULTAS AVANZADAS
@app.route('/prestamos/vencidos')
def usuarios_con_prestamos_vencidos():
    hoy = date.today()
    vencidos = (
        db.session.query(Usuario.nombre, Usuario.email, Prestamo.fecha_devolucion)
        .join(Prestamo)
        .filter(Prestamo.fecha_devolucion < hoy, Prestamo.devuelto == False)
        .all()
    )
    return render_template('prestamos_vencidos.html', vencidos=vencidos)

@app.route('/autor/mas-libros')
def autor_mas_libros():
    resultado = (
        db.session.query(Autor.nombre, db.func.count(Libro.id).label('total_libros'))
        .join(Libro)
        .group_by(Autor.id)
        .order_by(db.desc('total_libros'))
        .first()
    )
    autor = type('AutorStats', (object,), {})()
    autor.nombre = resultado[0] if resultado else None
    autor.total_libros = resultado[1] if resultado else 0
    return render_template('autor_mas_libros.html', autor=autor)

# EJECUTAR APP
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
