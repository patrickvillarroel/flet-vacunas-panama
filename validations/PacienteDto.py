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
    id: Optional[UUID] = None
    cedula: Optional[Annotated[str, Field(None,
                                          pattern="^(PE|E|N|[23456789](?:AV|PI)?|1[0123]?(?:AV|PI)?)-(\\d{1,4})-(\\d{1,6})$",
                                          max_length=15)]]
    pasaporte: Optional[Annotated[str, Field(..., pattern="^[A-Z0-9]{5,20}$", max_length=20)]] = None
    nombre: Optional[Annotated[str, Field(None, max_length=100)]]
    nombre2: Optional[Annotated[str, Field(None, max_length=100)]]
    apellido1: Optional[Annotated[str, Field(None, max_length=100)]]
    apellido2: Optional[Annotated[str, Field(None, max_length=100)]]
    correo: Optional[Annotated[EmailStr, Field(None, max_length=254)]]
    telefono: Optional[
        Annotated[PhoneNumber, Field(None, max_length=100, description="Número de teléfono en formato '+5076000000'")]]
    fecha_nacimiento: Annotated[datetime, Field(...)]
    edad: Optional[Annotated[int, Field(...)]] = None
    sexo: Annotated[str, Field('X', max_length=1, pattern="^[MFX]$",
                               description="Sexo permitos= M masculino, F femenino y X otros")]
    estado: Annotated[str, Field("NO_VALIDADO", max_length=50)]
    disabled: Annotated[bool, Field(True)]
    direccion: Optional[Annotated[DireccionDto, Field(...)]] = None
    usuario: Optional[Annotated[UsuarioDto, Field(None)]]

    @field_validator('telefono')
    def validate_telefono(cls, v: str) -> str:
        try:
            if v is not None:
                numero = parse(v)
                return format_number(numero, PhoneNumberFormat.E164)
        except NumberParseException:
            raise ValueError("Error al validar número de teléfono en formato E.164")

    @field_validator('fecha_nacimiento')
    def validate_fecha_nacimiento(cls, v: datetime) -> datetime:
        if v.date() > date.today():
            raise ValueError("La fecha debe ser hoy o en el pasado")
        return v


class VistaVacunaEnfermedad(BaseModel):
    vacuna: str
    enfermedades: Optional[list[dict]] = None
    sede: str
    dependencia: str
    id_vacuna: UUID
    numero_dosis: str
    edad_min_recomendada_meses: Optional[int] = None
    fecha_aplicacion: datetime
    intervalo_recomendado_dosis_dias: Optional[float] = None
    intervalo_real_dosis_dias: Optional[int] = None


def from_json_to_vista_vacuna_enfermedad(json_data: dict) -> VistaVacunaEnfermedad:
    return VistaVacunaEnfermedad(
        vacuna=json_data.get("vacuna"),
        enfermedades=json_data.get("enfermedades"),
        sede=json_data.get("sede"),
        dependencia=json_data.get("dependencia"),
        id_vacuna=json_data.get("id_vacuna"),
        numero_dosis=json_data.get("numero_dosis"),
        edad_min_recomendada_meses=json_data.get("edad_min_recomendada"),
        fecha_aplicacion=json_data.get("fecha_aplicacion"),
        intervalo_recomendado_dosis_dias=json_data.get("intervalo_recomendado_dosis"),
        intervalo_real_dosis_dias=json_data.get("intervalo_real_dosis")
    )
