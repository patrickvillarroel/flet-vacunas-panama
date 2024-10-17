from pydantic import BaseModel
from datetime import datetime


class ProvinciaDto(BaseModel):
    id: int
    nombre: str


class DistritoDto(BaseModel):
    id: int
    nombre: str
    provincia: ProvinciaDto


class DireccionDto(BaseModel):
    id: int
    direccion: str
    distrito: DistritoDto
    created_at: datetime
    updated_at: datetime
