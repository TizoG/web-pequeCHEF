from typing import List, Optional, Dict, Union
from pydantic import BaseModel, EmailStr


class CategoriasSchema(BaseModel):
    id: int
    nombre: str


class RecetasSchema(BaseModel):
    id: int
    titulo: str
    descripcion: str
    Dict[str, Union[str, List[str]]]
    categorias: List[str]
    imagen: str

    model_config = {"from_attributes": True}


class Respuestarecetas(BaseModel):
    recetas: List[RecetasSchema]


class Suscripcion(BaseModel):
    email: EmailStr
