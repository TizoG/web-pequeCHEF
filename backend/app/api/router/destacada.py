from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.models import Categorias, Ingredientes, RecetaIngredientes, Recetas, RecetaCategoria
from app.schemas import CategoriasSchema, RecetasSchema, Respuestarecetas
from app.db.crud import actualizar_receta_con_ingredientes, eliminar_receta
from datetime import datetime, timedelta, timezone

router = APIRouter()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.get("/destacada")
def receta_destacada(db: Session = Depends(get_db)):
    # Fecha actual
    ahora = datetime.now(timezone.utc)
    fecha_limite = ahora - timedelta(days=1)

    # Buscar la receta mas reciente( en las ultimas 24h)
    receta_destacada = db.query(Recetas).filter(
        Recetas.fecha_creacion > fecha_limite).order_by(Recetas.fecha_creacion.desc()).first()

    if not receta_destacada:
        # Si no hay recetas en las ultimas 24h, seleccionamos una aleatoria
        receta_destacada = db.query(Recetas).order_by(func.random()).first()

    if not receta_destacada:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    return {
        "id": receta_destacada.id,
        "titulo": receta_destacada.titulo,
        "descripcion": receta_destacada.descripcion,
        "imagen": receta_destacada.imagen
    }


@router.get("/destacada/nuevas")
def get_recetas_nuevas(db: Session = Depends(get_db), limit: int = 6):
    # Query para obtener las 6 recetas más recientes
    recetas = db.query(Recetas).order_by(
        Recetas.fecha_creacion.desc()).limit(limit).all()

    if not recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    return {"recetas": [
        {
            "id": receta.id,
            "titulo": receta.titulo,
            "descripcion": receta.descripcion,
            "imagen": receta.imagen
        }
        for receta in recetas
    ]}
