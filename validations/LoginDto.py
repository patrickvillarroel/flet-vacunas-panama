from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Set, Annotated

class PermisoDto(BaseModel):
    id: Optional[Annotated[int, Field()]] = None
    nombre: Annotated[str, Field(max_length=100, min_length=1)]
    descripcion: Optional[Annotated[str, Field(max_length=100, min_length=1)]] = None
    created_at: Optional[Annotated[datetime, Field()]] = None
    updated_at: Optional[Annotated[datetime, Field()]] = None

class RolDto(BaseModel):
    id: Optional[Annotated[int, Field()]] = None
    nombre: Annotated[str, Field(max_length=100, min_length=1)]
    descripcion: Optional[Annotated[str, Field(max_length=100, min_length=1)]] = None
    permisos: Annotated[Set[PermisoDto], Field(min_length=1)]
    created_at: Optional[Annotated[datetime, Field()]] = None
    updated_at: Optional[Annotated[datetime, Field()]] = None

class LoginInDto(BaseModel):
    username: Annotated[str, Field(..., min_length=1, max_length=50)]
    password: Annotated[str, Field(..., min_length=8, max_length=70)]

class UsuarioDto(BaseModel, LoginInDto):
    id: Optional[Annotated[UUID, Field()]] = None
    created_at: Optional[Annotated[datetime, Field()]] = None
    updated_at: Optional[Annotated[datetime, Field()]] = None
    last_used: Optional[Annotated[datetime, Field()]] = None
    roles: Set[RolDto] = Field(..., min_length=1)
    cedula: Optional[str] = Field(None, pattern="^(PE|E|N|[23456789](?:AV|PI)?|1[0123]?(?:AV|PI)?)-(\d{1,4})-(\d{1,6})$", max_length=15)
    pasaporte: Optional[str] = Field(None, pattern="^[A-Z0-9]{5,20}$", max_length=20)
    licencia_fabricante: Optional[str] = Field(None, pattern="^.+/DNFD$",max_length=50)
