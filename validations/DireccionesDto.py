from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProvinciaDto(BaseModel):
    id: int
    nombre: str


class DistritoDto(BaseModel):
    id: int
    nombre: str
    provincia: ProvinciaDto


class DireccionDto(BaseModel):
    id: Optional[UUID]
    direccion: str
    distrito: Optional[DistritoDto]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
