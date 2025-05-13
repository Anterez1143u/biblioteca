from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from models import Libro, Autor, Usuario, Prestamo
from database import Session as DBSession

# Crear sesión
def get_session():
    return DBSession()

# ---------------------------
# CRUD: AUTOR
# ---------------------------
def crear_autor(nombre, nacionalidad):
    session = get_session()
    autor = Autor(nombre=nombre, nacionalidad=nacionalidad)
    session.add(autor)
    session.commit()
    session.close()
    print("Autor creado.")

def listar_autores():
    session = get_session()
    autores = session.query(Autor).all()
    for a in autores:
        print(f"{a.id}: {a.nombre} - {a.nacionalidad}")
    session.close()

def actualizar_autor(autor_id, nombre=None, nacionalidad=None):
    session = get_session()
    autor = session.query(Autor).get(autor_id)
    if autor:
        if nombre:
            autor.nombre = nombre
        if nacionalidad:
            autor.nacionalidad = nacionalidad
        session.commit()
        print("Autor actualizado.")
    else:
        print("Autor no encontrado.")
    session.close()
def eliminar_autor(autor_id):
    session = get_session()
    autor = session.query(Autor).get(autor_id)
    if autor:
        session.delete(autor)
        session.commit()
        print("Autor eliminado.")
    else:
        print("Autor no encontrado.")
    session.close()
# ---------------------------
# CRUD: LIBRO
# ---------------------------
def crear_libro(titulo, genero, año, autor_id):
    session = get_session()
    libro = Libro(titulo=titulo, genero=genero, año_publicacion=año, autor_id=autor_id)
    session.add(libro)
    session.commit()
    session.close()
    print("Libro creado.")

def listar_libros():
    session = get_session()
    libros = session.query(Libro).all()
    for l in libros:
        print(f"{l.id}: {l.titulo} - {l.genero} - {l.año_publicacion}")
    session.close()
def actualizar_libro(libro_id, titulo=None, genero=None, año=None):
    session = get_session()
    libro = session.query(Libro).get(libro_id)
    if libro:
        if titulo:
            libro.titulo = titulo
        if genero:
            libro.genero = genero
        if año:
            libro.año_publicacion = año
        session.commit()
        print("Libro actualizado.")
    else:
        print("Libro no encontrado.")
    session.close()

def eliminar_libro(libro_id):
    session = get_session()
    libro = session.query(Libro).get(libro_id)
    if libro:
        session.delete(libro)
        session.commit()
        print("Libro eliminado.")
    else:
        print("Libro no encontrado.")
    session.close()
# ---------------------------
# CRUD: USUARIO
# ---------------------------
def crear_usuario(nombre, email, telefono):
    session = get_session()
    usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
    session.add(usuario)
    session.commit()
    session.close()
    print("Usuario creado.")

def listar_usuarios():
    session = get_session()
    usuarios = session.query(Usuario).all()
    for u in usuarios:
        print(f"{u.id}: {u.nombre} - {u.email} - {u.telefono}")
    session.close()
def actualizar_usuario(usuario_id, nombre=None, email=None, telefono=None):
    session = get_session()
    usuario = session.query(Usuario).get(usuario_id)
    if usuario:
        if nombre:
            usuario.nombre = nombre
        if email:
            usuario.email = email
        if telefono:
            usuario.telefono = telefono
        session.commit()
        print("Usuario actualizado.")
    else:
        print("Usuario no encontrado.")
    session.close()
def eliminar_usuario(usuario_id):
    session = get_session()
    usuario = session.query(Usuario).get(usuario_id)
    if usuario:
        session.delete(usuario)
        session.commit()
        print("Usuario eliminado.")
    else:
        print("Usuario no encontrado.")
    session.close()

# ---------------------------
# BÚSQUEDAS
# ---------------------------
def buscar_por_titulo(titulo):
    session = get_session()
    resultados = session.query(Libro).filter(Libro.titulo.ilike(f"%{titulo}%")).all()
    for libro in resultados:
        print(f"{libro.id}: {libro.titulo}")
    session.close()

def buscar_por_autor(nombre_autor):
    session = get_session()
    resultados = session.query(Libro).join(Autor).filter(Autor.nombre.ilike(f"%{nombre_autor}%")).all()
    for libro in resultados:
        print(f"{libro.id}: {libro.titulo} - Autor: {libro.autor.nombre}")
    session.close()

def buscar_por_genero(genero):
    session = get_session()
    resultados = session.query(Libro).filter(Libro.genero.ilike(f"%{genero}%")).all()
    for libro in resultados:
        print(f"{libro.id}: {libro.titulo} - Género: {libro.genero}")
    session.close()

def buscar_por_año(año):
    session = get_session()
    resultados = session.query(Libro).filter(Libro.año_publicacion == año).all()
    for libro in resultados:
        print(f"{libro.id}: {libro.titulo} - Año: {libro.año_publicacion}")
    session.close()

def autor_con_mas_libros():
    session = get_session()
    resultado = session.query(
        Autor.nombre,
        func.count(Libro.id).label('total_libros')
    ).join(Libro).group_by(Autor.id).order_by(func.count(Libro.id).desc()).first()
    
    session.close()

    if resultado:
        print(f"Autor con más libros: {resultado.nombre} ({resultado.total_libros} libros)")
    else:
        print("No hay autores con libros registrados.")

def libro_mas_prestado():
    session = get_session()
    resultado = session.query(
        Libro.titulo,
        func.count(Prestamo.id).label('total_prestamos')
    ).join(Prestamo).group_by(Libro.id).order_by(func.count(Prestamo.id).desc()).first()
    
    session.close()

    if resultado:
        print(f"Libro más prestado: {resultado.titulo} ({resultado.total_prestamos} préstamos)")
    else:
        print("No hay libros prestados registrados.")

def usuarios_con_prestamos_vencidos():
    session = get_session()
    hoy = date.today()

    prestamos_vencidos = session.query(
        Usuario.nombre,
        Usuario.email,
        Prestamo.fecha_devolucion
    ).join(Prestamo).filter(Prestamo.fecha_devolucion < hoy).all()

    session.close()

    if prestamos_vencidos:
        print("Usuarios con préstamos vencidos:")
        for nombre, email, fecha in prestamos_vencidos:
            print(f"- {nombre} ({email}) - Fecha de devolución: {fecha}")
    else:
        print("No hay préstamos vencidos.")        
# ---------------------------
# GESTIÓN DE PRÉSTAMOS
# ---------------------------
def registrar_prestamo(libro_id, usuario_id, fecha_prestamo, fecha_devolucion):
    session = get_session()
    prestamo = Prestamo(
        libro_id=libro_id,
        usuario_id=usuario_id,
        fecha_prestamo=fecha_prestamo,
        fecha_devolucion=fecha_devolucion
    )
    session.add(prestamo)
    session.commit()
    session.close()
    print("Préstamo registrado.")

def marcar_devolucion(prestamo_id):
    session = get_session()
    prestamo = session.query(Prestamo).get(prestamo_id)
    if prestamo:
        prestamo.fecha_devolucion = date.today()
        session.commit()
        print("Devolución registrada.")
    else:
        print("Préstamo no encontrado.")
    session.close()

def listar_prestamos_activos():
    session = get_session()
    hoy = date.today()
    prestamos = session.query(Prestamo).filter(Prestamo.fecha_devolucion > hoy).all()
    for p in prestamos:
        print(f"{p.id}: Libro: {p.libro.titulo}, Usuario: {p.usuario.nombre}, Devuelve: {p.fecha_devolucion}")
    session.close()

def crear_usuario(nombre, email, telefono, rol='lector'):
    session = get_session()
    usuario = Usuario(nombre=nombre, email=email, telefono=telefono, rol=rol)
    session.add(usuario)
    session.commit()
    session.close()
    print(f"Usuario '{nombre}' creado con rol '{rol}'.")

def login_usuario(email):
    session = get_session()
    usuario = session.query(Usuario).filter_by(email=email).first()
    if usuario:
        print(f"Bienvenido, {usuario.nombre} (Rol: {usuario.rol})")
        return usuario
    else:
        print("Usuario no encontrado.")
        return None
