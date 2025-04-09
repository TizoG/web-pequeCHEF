from sqlalchemy import JSON, CheckConstraint, Column, Enum, Integer, String, Table, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from .database import BASE


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
    tiempo_cocina = Column(JSON, nullable=False)
    dificultad = Column(Enum("Fácil", "Intermedio", "Difícil",
                        name="nivel_dificultad"), nullable=False)
    tags = Column(JSON, nullable=True)
    porciones = Column(Integer, nullable=False)
    tips = Column(JSON, nullable=True)

    # Relaciones
    # Relacion Many-to-Many con Categorias
    categoria = relationship(
        "Categorias",
        secondary="recetas_categorias",
        back_populates="recetas"
    )
    receta_ingredientes = relationship(
        "RecetaIngredientes", back_populates="receta", cascade="all, delete, delete-orphan", lazy="joined"
    )
    # recetas_alergias = relationship(
    #    "RecetaAlergias", back_populates="receta", cascade="all, delete",
    #    lazy="dynamic")
    valoraciones = relationship(
        "Valoraciones", back_populates="receta", cascade="all, delete")


class Categorias(BASE):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    # Relación Many-to-Many con Recetas a traves de una tabla intermedia
    recetas = relationship(
        "Recetas",
        secondary="recetas_categorias",
        back_populates="categoria",
        cascade="all, delete"
    )
    subcategorias = relationship(
        "Categorias", backref="parent", remote_side=[id])


# Tabla intermedia para la relacion Many-to-Many
recetas_categorias = Table(
    "recetas_categorias",
    BASE.metadata,
    Column("receta_id", Integer, ForeignKey(
        "recetas.id", ondelete="CASCADE"), primary_key=True),
    Column("categoria_id", Integer, ForeignKey(
        "categorias.id", ondelete="CASCADE"), primary_key=True)

)


class RecetaIngredientes(BASE):
    __tablename__ = "recetas_ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    ingrediente_id = Column(Integer, ForeignKey(
        "ingredientes.id", ondelete="CASCADE"))
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String(50), nullable=False)

    # Relaciones corregidas
    receta = relationship(
        "Recetas", back_populates="receta_ingredientes", cascade="all, delete")
    ingrediente = relationship(
        "Ingredientes", back_populates="receta_ingredientes", cascade="all, delete")


class Ingredientes(BASE):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)

    # Relación con RecetaIngredientes
    receta_ingredientes = relationship(
        "RecetaIngredientes", back_populates="ingrediente", cascade="all, delete")


"""class Alergias(BASE):
    __tablename__ = "alergias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), unique=True, nullable=False)

"""


"""class RecetaAlergias(BASE):
    __tablename__ = "receta_alergias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    receta_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    alergia_id = Column(Integer, ForeignKey("alergias.id", ondelete="CASCADE"))

    receta = relationship(
        "Recetas", back_populates="receta_alergias", cascade="all, delete")
    alergia = relationship(
        "Alergias", back_populates="receta_alergias", cascade="all, delete")
"""


class Valoraciones(BASE):
    __tablename__ = "valoraciones"
    id = Column(Integer, primary_key=True, autoincrement=True)
    recetas_id = Column(Integer, ForeignKey("recetas.id", ondelete="CASCADE"))
    puntuacion = Column(Integer, nullable=False)
    comentarios = Column(Text, nullable=True)
    fecha = Column(TIMESTAMP, nullable=False, index=True)

    # Restriccion para que la puntuación esté entre 1 y 5
    __table_args__ = (CheckConstraint(
        "puntuacion BETWEEN 1 AND 5", name="chk_puntuacion"),)

    # Relaciones
    receta = relationship("Recetas", back_populates="valoraciones")


class Suscriptores(BASE):
    __tablename__ = "suscriptores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    fecha_suscripcion = Column(TIMESTAMP, default=func.now())
