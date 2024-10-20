import logging
import os
from typing import List

import httpx
from dotenv import load_dotenv

from validations.ApiResponseDto import ApiResponseDto
from validations.DireccionesDto import DistritoDto, ProvinciaDto
from validations.PacienteDto import PacienteDto

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="assets/.env")
BASE_URL = os.getenv("BASE_URL")
if BASE_URL is None:
    raise RuntimeError("Base URL not set")


async def get_distritos() -> List[DistritoDto]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/public/distritos")
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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/public/provincias")
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


async def login_paciente(username: str, password: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/account/login", json={"username": username, "password": password})
            response_json = response.json()
            api_response = ApiResponseDto(**response_json)
            response.raise_for_status()
            return api_response.data
        except httpx.HTTPStatusError as exception:
            logger.error(f"Error en la solicitud login: {exception}")
            if api_response.errors:
                logger.error(api_response.errors)
            if api_response.warnings:
                logger.warning(api_response.warnings)
            return {"message": "Error al iniciar sesión", "error": exception}
        except Exception as e:
            logger.error(f"Error al obtener login. {e}")
            return {"message": "Error al obtener login", "error": "desconocido ver logs"}


async def register_paciente(paciente_dto: PacienteDto) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            paciente = paciente_dto.model_dump(mode="json", exclude_none=True)
            logger.debug(paciente)
            response = await client.post(f"{BASE_URL}/bulk/create/paciente-usuario-direccion", json=paciente)
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
            return {}
        except Exception as e:
            logger.error(f"Error al obtener paciente. {e}")
            return {}


async def refresh_tokens(refresh_token: str) -> dict:
    if not refresh_token or refresh_token.isspace():
        logging.error("Error al intentar refresh token token no dado")
        return {}
    headers = {"Authorization": f"Bearer {refresh_token}"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BASE_URL}/token/refresh", headers=headers)
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
