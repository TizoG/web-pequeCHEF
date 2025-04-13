from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.models import Categorias
from app.schemas import CategoriasSchema


router = APIRouter()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@router.get("/categorias")
def listar_categoria(db: Session = Depends(get_db)):
    db_categoria = db.query(Categorias).all()
    if not db_categoria:
        return []
    return [CategoriasSchema(id=categoria.id, nombre=categoria.nombre) for categoria in db_categoria]
