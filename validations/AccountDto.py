from datetime import datetime
from typing import Optional, Annotated, List
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class PermisoDto(BaseModel):
    id: Optional[Annotated[int, Field(None)]]
    nombre: Annotated[str, Field(..., max_length=100, min_length=1)]
    descripcion: Optional[Annotated[str, Field(..., max_length=100, min_length=1)]] = None
    created_at: Optional[Annotated[datetime, Field(...)]] = None
    updated_at: Optional[Annotated[datetime, Field(...)]] = None

    model_config = ConfigDict(frozen=True)


class RolDto(BaseModel):
    id: Optional[Annotated[int, Field(None)]]
    nombre: Optional[Annotated[str, Field(..., max_length=100, min_length=1)]] = None
    descripcion: Optional[Annotated[str, Field(..., max_length=100, min_length=1)]] = None
    permisos: Optional[Annotated[List[PermisoDto], Field(..., min_length=1, frozen=True)]] = None
    created_at: Optional[Annotated[datetime, Field(...)]] = None
    updated_at: Optional[Annotated[datetime, Field(...)]] = None

    model_config = ConfigDict(frozen=True)


class LoginInDto(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50)]
    password: Annotated[str, Field(..., min_length=8, max_length=70)]


class UsuarioDto(BaseModel):
    id: Optional[Annotated[UUID, Field(...)]] = None
    username: Optional[Annotated[str, Field(None, min_length=1)]] = None
    password: Optional[Annotated[str, Field(..., min_length=8, max_length=70)]] = None
    created_at: Optional[Annotated[datetime, Field(...)]] = None
    updated_at: Optional[Annotated[datetime, Field(...)]] = None
    last_used: Optional[Annotated[datetime, Field(...)]] = None
    roles: Annotated[List[RolDto], Field(..., min_length=1, frozen=True)]
