from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.models import Recetas
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
        query = query.filter(Recetas.categoria_id.in_(id_categoria))

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
            pasos=receta.pasos,
            categoria_id=receta.categoria_id,
            imagen=receta.imagen
        ))
    return Respuestarecetas(recetas=recetas_response)


@router.get("/recetas/categoria/{id_categoria}")
def recetas_por_categoria(id_categoria: int, db: Session = Depends(get_db)):
    db_recetas = db.query(Recetas).filter(
        Recetas.categoria_id == id_categoria).all()

    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    return Respuestarecetas(recetas=[RecetasSchema(**receta.__dict__) for receta in db_recetas])


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
