from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.models import Categorias, Ingredientes, RecetaIngredientes, Recetas
from app.schemas import RecetasSchema, Respuestarecetas
from app.db.crud import actualizar_receta_con_ingredientes, eliminar_receta

router = APIRouter()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.get("/recetas")
def all_recetas(id_categoria: Optional[List[int]] = None, nombre: Optional[str] = None, db: Session = Depends(get_db)):
    # Consulta de recetas basada en la presencia de id_categoria
    query = db.query(Recetas)

    if id_categoria:
        query = query.join(Recetas.categorias).filter(
            Categorias.id.in_(id_categoria))

    if nombre:
        query = query.filter(Recetas.titulo.ilike(f'%{nombre}%'))

    db_recetas = query.all()

    # Validar si no se encontraron recetas
    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    recetas_response = []
    for receta in db_recetas:
        recetas_response.append(RecetasSchema(
            id=receta.id,
            titulo=receta.titulo,
            descripcion=receta.descripcion,
            descripcion_original=receta.descripcion_original,
            pasos=receta.pasos,
            categorias=[
                relacion.categoria.nombre for relacion in receta.categorias],
            imagen=receta.imagen
        ))
    return Respuestarecetas(recetas=recetas_response)


@router.get("/recetas/categoria/{categoria_nombre}")
def recetas_por_categoria(categoria_nombre: str, db: Session = Depends(get_db)):
    db_recetas = db.query(Recetas).join(Recetas.categorias).join(Categorias).filter(
        func.lower(Categorias.nombre) == categoria_nombre.lower()
    ).all()

    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    return Respuestarecetas(
        recetas=[
            RecetasSchema(
                id=receta.id,
                titulo=receta.titulo,
                descripcion=receta.descripcion,
                pasos=receta.pasos,
                # Ajuste aquí
                categorias=[
                    relacion.categoria.nombre for relacion in receta.categorias],
                imagen=receta.imagen
            )
            for receta in db_recetas
        ]
    )


@router.put("/recetas/{receta_id}")
def actualizar_receta(
    receta_id: int,
    receta_data: RecetasSchema,
    db: Session = Depends(get_db)
):
    return actualizar_receta_con_ingredientes(
        db,
        receta_id,
        receta_data.categoria_id,
        receta_data.titulo,
        receta_data.descripcion,
        receta_data.pasos,
        receta_data.imagen,
        receta_data.lista_ingredientes
    )


@router.delete("/recetas/{receta_id}")
def borrar_receta(receta_id: int, db: Session = Depends(get_db)):
    return eliminar_receta(db, receta_id)


@router.get("/recetas/{receta_id}")
def recetas_id(receta_id: int, db: Session = Depends(get_db)):
    # Buscamos el id de la receta
    db_recetas = db.query(Recetas).filter(Recetas.id == receta_id).first()
    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    # Buscamos los ingredientes de la receta
    ingredientes = (
        db.query(Ingredientes.nombre, RecetaIngredientes.cantidad, RecetaIngredientes.unidad).join(
            RecetaIngredientes, RecetaIngredientes.ingrediente_id == Ingredientes.id).filter(
                RecetaIngredientes.receta_id == receta_id
        ).all()
    )

    lista_ingredientes = [
        {
            "nombre": ing[0],
            "cantidad": ing[1],
            "unidad": ing[2]
        }

        for ing in ingredientes
    ]
    return {
        "id": db_recetas.id,
        "titulo": db_recetas.titulo,
        "descripcion": db_recetas.descripcion,
        "descripcion_original": db_recetas.descripcion_original,
        "categoria": [relacion.categoria.nombre for relacion in db_recetas.categorias],
        "imagen": db_recetas.imagen,
        "pasos": db_recetas.pasos,
        "ingredientes": lista_ingredientes,
        "equipamiento": db_recetas.equipamiento,
        "valores_nutricionales": db_recetas.valores_nutricionales,
        "tiempo_cocina": db_recetas.tiempo_cocina,
        "dificultad": db_recetas.dificultad,
        "porciones": db_recetas.porciones
    }


@router.get("/recetas/search/{titulo}")
def nombre_receta(titulo: str, db: Session = Depends(get_db)):
    db_recetas = db.query(Recetas).filter(
        Recetas.titulo.ilike(f"%{titulo}%")).all()
    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )
    return Respuestarecetas(recetas=[RecetasSchema(**receta.__dict__) for receta in db_recetas])
