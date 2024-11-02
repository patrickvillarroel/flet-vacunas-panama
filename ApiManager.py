import logging
import os
from typing import List, Union
from uuid import UUID

import httpx
from dotenv import load_dotenv
from httpx import Response
from pydantic import ValidationError

from validations.AccountDto import LoginInDto
from validations.ApiResponseDto import ApiResponseDto
from validations.DireccionesDto import DistritoDto, ProvinciaDto
from validations.PacienteDto import PacienteDto

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="assets/.env")
BASE_URL = os.getenv("BASE_URL")
if BASE_URL is None:
    raise RuntimeError("Base URL not set")


async def get_distritos() -> List[DistritoDto]:
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.get("/public/distritos")
            response.raise_for_status()
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            distritos = [DistritoDto(**distrito) for distrito in api_response.data["distritos"]]
            return distritos
        except httpx.HTTPStatusError as execption:
            logger.error(execption)
            return []
        except Exception as e:
            logger.error(f"Error al obtener distritos. {e}")
            return []


async def get_provincias() -> List[ProvinciaDto]:
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.get("/public/provincias")
            response.raise_for_status()
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            provincias = [ProvinciaDto(**provincia) for provincia in api_response.data["provincias"]]
            return provincias
        except httpx.HTTPStatusError as exception:
            logger.error(exception)
            return []
        except Exception as e:
            logger.error(f"Error al obtener provincias. {e}")
            return []


async def login(login_dto: Union[LoginInDto, None] = None,
                username: Union[str, None] = None,
                password: Union[str, None] = None) -> dict:
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            if login_dto:
                login_json = login_dto.model_dump(mode="json", exclude_none=True)
            elif username and password:
                login_dto = LoginInDto(username=username, password=password)
                login_json = login_dto.model_dump(mode="json", exclude_none=True)
            else:
                raise ValueError("Debe proporcionar un DTO o strings para hacer login")
            response = await client.post("/account/login", json=login_json)
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            response.raise_for_status()
            if response.status_code == 301:
                return {"message": "Se ha recibido un redireccionamiento, posible riesgo de contraseña",
                        "error": response}
            return api_response.data
        except httpx.HTTPStatusError as exception:
            logger.error(f"Error en la solicitud login: {exception}")
            if api_response.errors:
                logger.error(api_response.errors)
            if api_response.warnings:
                logger.warning(api_response.warnings)
            return {"message": "Error al iniciar sesión", "error": exception}
        except ValidationError as exception:
            logger.error(f"Error al convertir a DTO: {exception}")
            return {"message": "Validación fallida. Intente nuevamente", "error": exception}
        except Exception as e:
            logger.error(f"Error al obtener login. {e}")
            return {"message": "Error al conectarse al servidor", "error": e}


async def register_paciente(paciente_dto: PacienteDto) -> dict:
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            paciente = paciente_dto.model_dump(mode="json", exclude_none=True)
            logger.debug(paciente)
            response = await client.post("/bulk/paciente-usuario-direccion", json=paciente)
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            response.raise_for_status()
            return api_response.data
        except httpx.HTTPStatusError as exception:
            logger.error(exception)
            if api_response.errors:
                logger.error(api_response.errors)
            if api_response.warnings:
                logger.warning(api_response.warnings)
            return {"error": exception, "message": "Ha ocurrido un error, revise sus datos y si no este registrado"}
        except Exception as e:
            logger.error(f"Error al obtener paciente. {e}")
            return {"error": e, "message": "Ha ocurrido un error, reintente luego"}


async def get_vista_paciente_vacuna_enfermedad(token: str) -> dict:
    if not token or token.isspace():
        logging.error("Error al intentar obtener vista paciente, token no suministrado")
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.get("/patient", headers=headers)
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            response.raise_for_status()
            return api_response.data
        except httpx.HTTPStatusError as exception:
            logger.error(exception)
            if api_response.errors:
                logger.error(api_response.errors)
            if api_response.warnings:
                logger.warning(api_response.warnings)
            if exception.response.status_code == 401:
                return {"error": "Acceso no autorizado",
                        "message": "Error al intentar acceder a sus datos, reintentando..."}
            else:
                return {"error": exception, "message": "Ha ocurrido un error"}
        except Exception as e:
            logger.error(f"Error al obtener vista paciente. {e}")
            return {"error": e, "message": "Error, reintente luego"}


async def get_pdf_file_paciente(id_paciente: UUID, id_vacuna: UUID) -> Response | None:
    if id_paciente and id_vacuna:
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            try:
                response = await client.get(f"/pdf?idVacuna={id_vacuna}&idPaciente={id_paciente}")
                response.raise_for_status()
            except httpx.HTTPStatusError as exception:
                logger.error(exception)
                return None
            except Exception as e:
                logger.error(f"Error al obtener PDF de paciente. {e}")
                return None
            return response
    else:
        logger.error("Error al intentar pedir PDF paciente, ID's no dados")
        return None


# TODO cambiar por httpx.Auth flow
async def refresh_tokens(refresh_token: str) -> dict:
    if not refresh_token or refresh_token.isspace():
        logging.error("Error al intentar refresh token token no dado")
        return {}
    headers = {"Authorization": f"Bearer {refresh_token}"}
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        try:
            response = await client.post("/token/refresh", headers=headers)
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            response.raise_for_status()
            return api_response.data
        except httpx.HTTPStatusError as exception:
            logger.error(exception)
            if api_response.errors:
                logger.error(api_response.errors)
            if api_response.warnings:
                logger.warning(api_response.warnings)
            return {"error": "No se pudo volver a acceder a los datos"}
        except Exception as e:
            logger.error(f"Error al refrescar token. {e}")
            return {"error": "Error inesperado"}
