from typing import List, Optional, Dict
from pydantic import BaseModel, EmailStr


class CategoriasSchema(BaseModel):
    id: int
    nombre: str


class RecetasSchema(BaseModel):
    id: int
    titulo: str
    descripcion: str
    pasos: Dict[str, str]
    categorias: List[str]
    imagen: str

    model_config = {"from_attributes": True}


class Respuestarecetas(BaseModel):
    recetas: List[RecetasSchema]


class Suscripcion(BaseModel):
    email: EmailStr
