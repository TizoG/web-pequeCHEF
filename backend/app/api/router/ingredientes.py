from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.models import Ingredientes, Recetas, RecetaIngredientes
from app.schemas import Respuestarecetas, RecetasSchema


router = APIRouter()


def get_bd():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# TODO: Podemos optimizar la primera consulta consultando solo los IDs, con .with_entities(RecetaIngredientes.receta_id)


@router.get("/recetas/{ingrediente}")
def listar_recetas_ingredientes(ingredientes: str, db: Session = Depends(get_bd)):

    lista_ingredientes = ingredientes.split(",")

    ingredientes_ids = db.query(Ingredientes.id).filter(
        Ingredientes.nombre.in_(lista_ingredientes)).all()

    if not ingredientes_ids:
        raise HTTPException(
            status_code=404, details="No se encontraron ingredientes")

    # Obtener IDs como lista
    ids = [id[0] for id in ingredientes_ids]

    # Buscar recetas que usen esos ingredientes
    recetas_ids = db.query(RecetaIngredientes.receta_id).filter(
        RecetaIngredientes.ingrediente_id.in_(ids)).distinct().all()

    if not recetas_ids:
        raise HTTPException(
            status_code=404, details="No se encontraron recetas")

    # Convertir a lista simple de IDs
    recetas_ids = [id[0] for id in recetas_ids]

    # Obtener recetas finales
    db_recetas = db.query(Recetas).filter(Recetas.id.in_(recetas_ids)).all()

    return Respuestarecetas(recetas=[RecetasSchema(**receta.__dict__) for receta in db_recetas])
