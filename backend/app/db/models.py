from sqlalchemy import CheckConstraint, Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import BASE


# Creamos las tablas
class Recetas(BASE):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String,  index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    pasos = Column(Text, nullable=False)
    categoria_id = Column(Integer, ForeignKey(
        "categorias.id", ondelete="CASCADE"))
    imagen = Column(String)

    # Relaciones
    categoria = relationship("Categorias", back_populates="recetas")
    receta_ingredientes = relationship(
        "RecetaIngredientes", back_populates="receta", cascade="all, delete")
    # recetas_alergias = relationship(
    #    "RecetaAlergias", back_populates="receta", cascade="all, delete",
    #    lazy="dynamic")
    valoraciones = relationship(
        "Valoraciones", back_populates="receta", cascade="all, delete")


class Categorias(BASE):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)

    # Relación con Recetas
    recetas = relationship(
        "Recetas", back_populates="categoria", cascade="all, delete")


class RecetaIngredientes(BASE):
    __tablename__ = "recetas_ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    ingrediente_id = Column(Integer, ForeignKey(
        "ingredientes.id", ondelete="CASCADE"))
    cantidad = Column(String, nullable=False)
    unidad = Column(String, nullable=False)

    # Relaciones corregidas
    receta = relationship(
        "Recetas", back_populates="receta_ingredientes", cascade="all, delete")
    ingrediente = relationship(
        "Ingredientes", back_populates="receta_ingredientes", cascade="all, delete")


class Ingredientes(BASE):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)

    # Relación con RecetaIngredientes
    receta_ingredientes = relationship(
        "RecetaIngredientes", back_populates="ingrediente", cascade="all, delete")


class Alergias(BASE):
    __tablename__ = "alergias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)


class RecetaAlergias(BASE):
    __tablename__ = "receta_alergias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    alergia_id = Column(Integer, ForeignKey("alergias.id", ondelete="CASCADE"))

    # Relaciones corregidas
    # receta = relationship(
    #    "Recetas", back_populates="receta_alergias", cascade="all, delete")
    # alergia = relationship(
    #    "Alergias", back_populates="receta_alergias", cascade="all, delete")


class Valoraciones(BASE):
    __tablename__ = "valoraciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recetas_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    puntuacion = Column(Integer, nullable=False)
    comentarios = Column(Text, nullable=True)
    fecha = Column(TIMESTAMP, nullable=False)

    # Restriccion para que la puntuación esté entre 1 y 5
    __table_args__ = (CheckConstraint(
        "puntuacion BETWEEN 1 AND 5", name="chk_puntuacion"),)

    # Relaciones
    receta = relationship("Recetas", back_populates="valoraciones")
