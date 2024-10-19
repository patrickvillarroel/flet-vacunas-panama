from datetime import datetime, date
from typing import Optional, Annotated
from uuid import UUID

from phonenumbers import parse
from phonenumbers.phonenumberutil import format_number, PhoneNumberFormat, NumberParseException
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from validations.AccountDto import UsuarioDto
from validations.DireccionesDto import DireccionDto


class PacienteDto(BaseModel):
    id: UUID
    cedula: Optional[Annotated[str, Field(...,
                                          pattern="^(PE|E|N|[23456789](?:AV|PI)?|1[0123]?(?:AV|PI)?)-(\\d{1,4})-(\\d{1,6})$",
                                          max_length=15)]]
    pasaporte: Optional[Annotated[str, Field(..., pattern="^[A-Z0-9]{5,20}$", max_length=20)]]
    nombre: Optional[Annotated[str, Field(..., max_length=100)]]
    nombre2: Optional[Annotated[str, Field(..., max_length=100)]]
    apellido1: Optional[Annotated[str, Field(..., max_length=100)]]
    apellido2: Optional[Annotated[str, Field(..., max_length=100)]]
    correo: Optional[Annotated[EmailStr, Field(..., max_length=254)]]
    telefono: Optional[
        Annotated[PhoneNumber, Field(..., max_length=100, description="Número de teléfono en formato '+5076000000'")]]
    fecha_nacimiento: Annotated[datetime, Field(...)]
    edad: Optional[Annotated[int, Field(...)]]
    sexo: Annotated[str, Field(..., max_length=1, pattern="^[MFX]$",
                               description="Sexo permitos= M masculino, F femenino y X otros")]
    estado: Annotated[str, Field("NO_VALIDADO", max_length=50)]
    disabled: Annotated[bool, Field(False)]
    direccion: Optional[Annotated[DireccionDto, Field(...)]]
    usuario: Optional[Annotated[UsuarioDto, Field(...)]]

    @field_validator('telefono')
    def validate_telefono(cls, v: str) -> str:
        try:
            numero = parse(v)
            return format_number(numero, PhoneNumberFormat.E164)
        except NumberParseException:
            raise ValueError("Error al validar número de teléfono en formato E.164")

    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, v: datetime) -> datetime:
        if v.date() > date.today():
            raise ValueError("La fecha debe ser hoy o en el pasado")
        return v
