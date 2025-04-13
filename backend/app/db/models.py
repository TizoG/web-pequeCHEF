from sqlalchemy import JSON, CheckConstraint, Column, Enum, Integer, String, Table, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import BASE
from sqlalchemy.ext.associationproxy import association_proxy

# Creamos las tablas


class Recetas(BASE):
    __tablename__ = "recetas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255),  index=True, nullable=False)
    descripcion = Column(Text, nullable=False)
    descripcion_original = Column(Text, nullable=False)
    pasos = Column(JSON, nullable=False)
    imagen = Column(String(255), nullable=False)
    preparacion_previa = Column(JSON, nullable=True)
    equipamiento = Column(JSON, nullable=True)
    valores_nutricionales = Column(JSON, nullable=False)
    tiempo_cocina = Column(String(100), nullable=False)
    dificultad = Column(Enum("Fácil", "Intermedio", "Difícil",
                        name="nivel_dificultad"), nullable=False)
    tags = Column(JSON, nullable=True)
    porciones = Column(Integer, nullable=False)
    tips = Column(JSON, nullable=True)
    fecha_creacion = Column(
        TIMESTAMP, server_default=func.now(), nullable=False)

    # Relaciones
    # Relación Many-to-Many con Categorias
    categorias = association_proxy("recetas_categorias", "categoria")

    # Relación con RecetaIngredientes
    receta_ingredientes = relationship(
        "RecetaIngredientes",
        back_populates="receta",
        cascade="all, delete-orphan"
    )

    valoraciones = relationship(
        "Valoraciones", back_populates="receta", cascade="all, delete")

    ingredientes = association_proxy("receta_ingredientes", "ingrediente",
                                     creator=lambda ingrediente: RecetaIngredientes(ingrediente=ingrediente))
    recetas_categorias = relationship(
        "RecetaCategoria",
        back_populates="receta",
        cascade="all, delete-orphan"
    )


class Categorias(BASE):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)

    # Relación Many-to-Many con Recetas a través de una tabla intermedia
    recetas = association_proxy("recetas_categorias", "receta")

    # Relación para subcategorías
    subcategorias = relationship(
        "Categorias", backref="parent", remote_side=[id])
    recetas_categorias = relationship(
        "RecetaCategoria",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )
    subcategorias = relationship(
        "Categorias", backref="parent", remote_side=[id])

# Tabla intermedia para la relación Many-to-Many entre Recetas y Categorias


class RecetaCategoria(BASE):
    __tablename__ = "recetas_categorias"
    receta_id = Column(Integer, ForeignKey(
        "recetas.id", ondelete="CASCADE"), primary_key=True)
    categoria_id = Column(Integer, ForeignKey(
        "categorias.id", ondelete="CASCADE"), primary_key=True)

    # Relaciones
    receta = relationship("Recetas", back_populates="recetas_categorias")
    categoria = relationship(
        "Categorias", back_populates="recetas_categorias")


class RecetaIngredientes(BASE):
    __tablename__ = "recetas_ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    ingrediente_id = Column(Integer, ForeignKey(
        "ingredientes.id", ondelete="CASCADE"))
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String(50), nullable=False)

    # Relaciones corregidas
    receta = relationship("Recetas", back_populates="receta_ingredientes")
    ingrediente = relationship(
        "Ingredientes", back_populates="receta_ingredientes")


class Ingredientes(BASE):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)

    # Relación con RecetaIngredientes
    receta_ingredientes = relationship(
        "RecetaIngredientes", back_populates="ingrediente", cascade="all, delete-orphan"
    )
    # Relación Many-to-Many con Recetas
    recetas = association_proxy("receta_ingredientes", "receta",
                                creator=lambda receta: RecetaIngredientes(receta=receta))


class Valoraciones(BASE):
    __tablename__ = "valoraciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recetas_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    puntuacion = Column(Integer, nullable=False)
    comentarios = Column(Text, nullable=True)
    fecha = Column(TIMESTAMP, nullable=False, index=True)

    # Restricción para que la puntuación esté entre 1 y 5
    __table_args__ = (CheckConstraint(
        "puntuacion BETWEEN 1 AND 5", name="chk_puntuacion"),)

    # Relaciones
    receta = relationship("Recetas", back_populates="valoraciones")


class Suscriptores(BASE):
    __tablename__ = "suscriptores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    fecha_suscripcion = Column(TIMESTAMP, default=func.now())
