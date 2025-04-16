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
        categorias_completas = [
            Categorias(id=c.id, nombre=c.nombre) for c in receta.categorias
        ]
        recetas_response.append(RecetasSchema(
            id=receta.id,
            titulo=receta.titulo,
            descripcion=receta.descripcion,
            descripcion_original=receta.descripcion_original,
            pasos=receta.pasos,
            categorias=categorias_completas,
            imagen=receta.imagen,
            tiempo_cocina=receta.tiempo_cocina
        ))
    return {"recetas": recetas_response}


@router.get("/recetas/categoria/{categoria_nombre}", response_model=Respuestarecetas)
def recetas_por_categoria(categoria_nombre: str, db: Session = Depends(get_db)):
    db_recetas = db.query(Recetas).filter(Recetas.recetas_categorias.any(
        RecetaCategoria.categoria.has(Categorias.nombre == categoria_nombre))).all()

    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    return {"recetas": db_recetas}


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
        receta_data.lista_ingredientes,
        receta_data.tiempo_cocina
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
    categorias = [{"id": c.id, "nombre": c.nombre}
                  for c in db_recetas.categorias]
    return {
        "id": db_recetas.id,
        "titulo": db_recetas.titulo,
        "descripcion": db_recetas.descripcion,
        "descripcion_original": db_recetas.descripcion_original,
        "categoria": categorias,
        "imagen": db_recetas.imagen,
        "pasos": db_recetas.pasos,
        "ingredientes": lista_ingredientes,
        "equipamiento": db_recetas.equipamiento,
        "valores_nutricionales": db_recetas.valores_nutricionales,
        "tiempo_cocina": db_recetas.tiempo_cocina,
        "dificultad": db_recetas.dificultad,
        "porciones": db_recetas.porciones,

    }


@router.get("/recetas/search/{titulo}")
def nombre_receta(titulo: str, db: Session = Depends(get_db)):

    db_recetas = db.query(Recetas).filter(
        Recetas.titulo.ilike(f"%{titulo}%")).all()

    if not db_recetas:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )
    return Respuestarecetas(recetas=[
        RecetasSchema(
            id=receta.id,
            titulo=receta.titulo,
            descripcion=receta.descripcion,
            descripcion_original=receta.descripcion_original,
            pasos=receta.pasos,
            categorias=[CategoriasSchema(id=c.id, nombre=c.nombre)
                        for c in receta.categorias],
            imagen=receta.imagen,
            tiempo_cocina=receta.tiempo_cocina
        )
        for receta in db_recetas
    ])


@router.get("/recetas/destacada")
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


@router.get("/recetas/categoria/{categoria_nombre}")
def recetas_por_categorias(categoria_nombre: str, db: Session = Depends(get_db)):
    db_categorias = db.query(Categorias).filter(
        Categorias.nombre == categoria_nombre).first()

    if not db_categorias:
        raise HTTPException(
            status_code=404, detail="No tenemos ninguna receta."
        )

    recetas = db.query(Recetas).join(Recetas.categorias).filter(
        Categorias.id == db_categorias.id).all()

    return {"recetas": recetas}
