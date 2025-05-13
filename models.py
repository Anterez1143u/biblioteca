from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

from database import db

class Libro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50))
    anio_publicacion = db.Column(db.Integer)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'))

class Autor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    libros = db.relationship('Libro', backref='autor', lazy=True)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Prestamo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    libro_id = db.Column(db.Integer, db.ForeignKey('libro.id'))
    fecha_prestamo = db.Column(db.Date)
    fecha_devolucion = db.Column(db.Date)
