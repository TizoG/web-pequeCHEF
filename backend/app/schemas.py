from typing import List, Optional, Dict, Union
from pydantic import BaseModel, EmailStr


class CategoriasSchema(BaseModel):
    id: int
    nombre: str
    model_config = {"from_attributes": True}


class RecetasSchema(BaseModel):
    id: int
    titulo: str
    descripcion: str
    pasos: Dict[str, Union[str, List[str]]]  # Ahora sí esto está bien
    categorias: List[CategoriasSchema]
    imagen: str
    tiempo_cocina: str

    model_config = {"from_attributes": True}


class Respuestarecetas(BaseModel):
    recetas: List[RecetasSchema]


class Suscripcion(BaseModel):
    email: EmailStr
