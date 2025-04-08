from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.db.crud import suscriptor
from app.db.models import Suscriptores
from sqlalchemy.orm import Session
from app.db.database import session_local
from app.schemas import Suscripcion

app = FastAPI()

router = APIRouter()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


"""@app.post("/suscribirse")
def suscribirse(email: str, db: Session = Depends(get_db)):
    return suscriptor(db, email)
"""


@router.post("/suscribirse")
def suscribirse(suscripcion: Suscripcion, db: Session = Depends(get_db)):
    email = suscripcion.email
    db_suscriptor = db.query(Suscriptores).filter_by(email=email).first()
    if db_suscriptor:
        raise HTTPException(
            status_code=400, detail="Este email ya está registrado."
        )
    try:
        nuevo_suscriptor = Suscriptores(email=email)
        db.add(nuevo_suscriptor)
        db.commit()
        return {"mensaje": "Te has suscrito correctamente.", "email": nuevo_suscriptor.email}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
