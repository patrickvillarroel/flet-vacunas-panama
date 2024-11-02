from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProvinciaDto(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None


class DistritoDto(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    provincia: Optional[ProvinciaDto] = None


class DireccionDto(BaseModel):
    id: Optional[UUID] = None
    direccion: Optional[str] = None
    distrito: Optional[DistritoDto] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
