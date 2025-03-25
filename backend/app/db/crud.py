from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Categorias, Ingredientes, Recetas, RecetaIngredientes

# Agregar una receta con sus ingredientes


def insertar_receta_con_ingredientes(
    db: Session,
    categoria_nombre: str,
    titulo: str,
    descripcion: str,
    pasos: str,
    imagen: str,
    lista_ingredientes: list
):
    # Verificar o crear la categoría
    categoria = db.query(Categorias).filter_by(nombre=categoria_nombre).first()
    if not categoria:
        categoria = Categorias(nombre=categoria_nombre)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

    # Crear la receta vinculada a la categoría
    receta = Recetas(
        titulo=titulo,
        descripcion=descripcion,
        pasos=pasos,
        categoria_id=categoria.id,
        imagen=imagen
    )
    db.add(receta)
    db.commit()
    db.refresh(receta)  # Obtener el ID asignado

    # Manejar los ingredientes
    for data_ingrediente in lista_ingredientes:
        # Extraemos nombre, cantidad y unidad
        nombre = data_ingrediente["nombre"]
        # si no ponemos nada introducimos valor por defecto
        cantidad = data_ingrediente.get("cantidad", 1)
        unidad = data_ingrediente.get("unidad", "unidad")

        # Verificar si el ingrediente ya existe
        ingrediente = db.query(Ingredientes).filter_by(
            nombre=nombre).first()
        if not ingrediente:
            # Crear el ingrediente si no existe
            ingrediente = Ingredientes(nombre=nombre)
            db.add(ingrediente)
            db.commit()
            db.refresh(ingrediente)

        # Relacionar receta con ingrediente incluyendo cantidad y unidad
        receta_ingrediente = RecetaIngredientes(
            receta_id=receta.id,
            ingrediente_id=ingrediente.id,
            cantidad=cantidad,
            unidad=unidad
        )
        db.add(receta_ingrediente)

    # Confirmar las relaciones
    db.commit()

    # Retornar un mensaje o los detalles
    return {
        "mensaje": "Receta insertada con éxito",
        "receta": {
            "titulo": receta.titulo,
            "categoria": categoria.nombre,
            "ingredientes": lista_ingredientes
        }
    }


def insertar_receta_con_ingredientes(
    db: Session,
    categoria_nombre: str,
    titulo: str,
    descripcion: str,
    pasos: str,
    imagen: str,
    lista_ingredientes: list
):
    # Verificar o crear la categoría
    categoria = db.query(Categorias).filter_by(nombre=categoria_nombre).first()
    if not categoria:
        categoria = Categorias(nombre=categoria_nombre)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

    # Crear la receta vinculada a la categoría
    receta = Recetas(
        titulo=titulo,
        descripcion=descripcion,
        pasos=pasos,
        categoria_id=categoria.id,
        imagen=imagen
    )
    db.add(receta)
    db.commit()
    db.refresh(receta)  # Obtener el ID asignado

    # Manejar los ingredientes
    for data_ingrediente in lista_ingredientes:
        # Extraemos nombre, cantidad y unidad
        nombre = data_ingrediente["nombre"]
        # si no ponemos nada introducimos valor por defecto
        cantidad = data_ingrediente.get("cantidad", 1)
        unidad = data_ingrediente.get("unidad", "unidad")

        # Verificar si el ingrediente ya existe
        ingrediente = db.query(Ingredientes).filter_by(
            nombre=nombre).first()
        if not ingrediente:
            # Crear el ingrediente si no existe
            ingrediente = Ingredientes(nombre=nombre)
            db.add(ingrediente)
            db.commit()
            db.refresh(ingrediente)

        # Relacionar receta con ingrediente incluyendo cantidad y unidad
        receta_ingrediente = RecetaIngredientes(
            receta_id=receta.id,
            ingrediente_id=ingrediente.id,
            cantidad=cantidad,
            unidad=unidad
        )
        db.add(receta_ingrediente)

    # Confirmar las relaciones
    db.commit()

    # Retornar un mensaje o los detalles
    return {
        "mensaje": "Receta insertada con éxito",
        "receta": {
            "titulo": receta.titulo,
            "categoria": categoria.nombre,
            "ingredientes": lista_ingredientes
        }
    }


# Actualizar recetas

def actualizar_receta_con_ingredientes(
        db: Session,
        receta_id: int,
        categoria_nombre: str,
        titulo: str,
        descripcion: str,
        pasos: str,
        imagen: str,
        lista_ingredientes: list
):
    # Buscar la receta
    receta = db.query(Recetas).filter_by(id=receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )

    # Verificar o crear la categoría
    categoria = db.query(Categorias).filter_by(nombre=categoria_nombre).first()
    if not categoria:
        categoria = Categorias(nombre=categoria_nombre)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

    # Actualizar los datos de la receta
    receta.titulo = titulo
    receta.descripcion = descripcion
    receta.pasos = pasos
    receta.categoria_id = categoria.id
    receta.imagen = imagen

    # eliminar los igredientes antiguos
    db.query(RecetaIngredientes).filter_by(receta_id=receta.id).delete()

    # Insertar los nuevos ingredientes
    for data_ingrediente in lista_ingredientes:
        nombre = data_ingrediente["nombre"]
        cantidad = data_ingrediente.get("cantidad", 1)
        unidad = data_ingrediente.get("unidad", "unidad")

    # Verificar si el ingrediente ya existe
    ingrediente = db.query(Ingredientes).filter_by(nombre=nombre).first()
    if not ingrediente:
        ingrediente = Ingredientes(nombre=nombre)
        db.add(ingrediente)
        db.commit()
        db.refresh(ingrediente)

    # Relacionar con la receta
    receta_ingrediente = RecetaIngredientes(
        receta_id=receta.id,
        ingrediente_id=ingrediente.id,
        cantidad=cantidad,
        unidad=unidad
    )
    db.add(receta_ingrediente)
    db.commit()
    return {"mensaje": "Receta actualizada con exito."}


# Borrar recetas
def eliminar_receta(db: Session, receta_id: int):
    receta = db.query(Recetas).filter_by(id=receta_id).first()
    if not receta:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )
    db.delete(receta)
    db.commit()
    return {"mensaje": "Receta eliminada con exito."}
