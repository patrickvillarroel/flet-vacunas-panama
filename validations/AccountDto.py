from datetime import datetime
from typing import Optional, Annotated, List
from uuid import UUID

from pydantic import BaseModel, Field


class PermisoDto(BaseModel):
    id: Optional[Annotated[int, Field(...)]]
    nombre: Annotated[str, Field(max_length=100, min_length=1)]
    descripcion: Optional[Annotated[str, Field(max_length=100, min_length=1)]]
    created_at: Optional[Annotated[datetime, Field(...)]]
    updated_at: Optional[Annotated[datetime, Field(...)]]

    class Config:
        frozen = True


class RolDto(BaseModel):
    id: Optional[Annotated[int, Field(...)]]
    nombre: Optional[Annotated[str, Field(max_length=100, min_length=1)]]
    descripcion: Optional[Annotated[str, Field(max_length=100, min_length=1)]]
    permisos: Optional[Annotated[List[PermisoDto], Field(min_length=1, frozen=True)]]
    created_at: Optional[Annotated[datetime, Field(...)]]
    updated_at: Optional[Annotated[datetime, Field(...)]]

    class Config:
        frozen = True


class LoginInDto(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50)]
    password: Annotated[str, Field(..., min_length=8, max_length=70)]


class UsuarioDto(BaseModel):
    id: Optional[Annotated[UUID, Field(...)]]
    username: Optional[Annotated[str, Field(min_length=1)]]
    password: Optional[Annotated[str, Field(min_length=8, max_length=70)]] = None
    created_at: Optional[Annotated[datetime, Field(...)]]
    updated_at: Optional[Annotated[datetime, Field(...)]]
    last_used: Optional[Annotated[datetime, Field(...)]]
    roles: Annotated[List[RolDto], Field(..., min_length=1, frozen=True)]
    cedula: Optional[Annotated[str, Field(...,
                                          pattern="^(PE|E|N|[23456789](?:AV|PI)?|1[0123]?(?:AV|PI)?)-(\\d{1,4})-(\\d{1,6})$",
                                          max_length=15)]] = None
    pasaporte: Optional[Annotated[str, Field(..., pattern="^[A-Z0-9]{5,20}$", max_length=20)]] = None
    licencia_fabricante: Optional[Annotated[str, Field(..., pattern="^.+/DNFD$", max_length=50)]] = None
