import asyncio
import logging
import os
import threading
import time
from typing import List, Union, Generator, AsyncGenerator
from uuid import UUID

import httpx
from dotenv import load_dotenv
from httpx import Request, Response
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


class ApiAuthentication(httpx.Auth):
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = time.time() + 3600
        self._sync_lock = threading.RLock()
        self._async_lock = asyncio.Lock()

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        response = yield request

        if response.status_code == 401:
            self.refresh_tokens()
            request.headers["Authorization"] = f"Bearer {self.access_token}"
            yield request

    def refresh_tokens(self) -> None:
        with self._sync_lock:
            headers = {"Authorization": f"Bearer {self.refresh_token}"}
            try:
                if time.time() >= self.token_expiry:
                    with httpx.Client(base_url=BASE_URL) as client:
                        response = client.post("/token/refresh", headers=headers)
                        response_json = response.json()
                        api_response = ApiResponseDto(**response_json)
                        response.raise_for_status()
                        self.access_token = response_json["access_token"]
                        self.refresh_token = response_json["refresh_token"]
                        self.token_expiry = time.time() + 3600
            except httpx.HTTPStatusError as e:
                logger.exception(e)
                if api_response.errors:
                    logger.error(api_response.errors)
                if api_response.warnings:
                    logger.warning(api_response.warnings)
            except Exception as e:
                logger.exception(e)

    async def async_auth_flow(self, request: Request) -> AsyncGenerator[Request, Response]:
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        response = yield request

        if response.status_code == 401:
            await self.async_refresh_tokens()
            request.headers["Authorization"] = f"Bearer {self.access_token}"
            yield request

    async def async_refresh_tokens(self) -> None:
        async with self._async_lock:
            headers = {"Authorization": f"Bearer {self.refresh_token}"}
            async with httpx.AsyncClient(base_url=BASE_URL) as client:
                try:
                    if time.time() >= self.token_expiry:
                        response = await client.post("/token/refresh", headers=headers)
                        response_json = response.json()
                        api_response = ApiResponseDto(**response_json)
                        response.raise_for_status()
                        self.access_token = api_response.data.get("access_token")
                        self.refresh_token = api_response.data.get("refresh_token")
                        self.token_expiry = time.time() + 3600
                except httpx.HTTPStatusError as exception:
                    logger.exception(exception)
                    if api_response.errors:
                        logger.error(api_response.errors)
                    if api_response.warnings:
                        logger.warning(api_response.warnings)
                except Exception as e:
                    logger.exception(f"Error al refrescar token. {e}")


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


async def get_vista_paciente_vacuna_enfermedad(async_client: ApiAuthentication) -> dict:
    async with httpx.AsyncClient(base_url=BASE_URL, auth=async_client) as client:
        try:
            response = await client.get("/patient")
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
            if response.status_code == 404:
                return api_response.data
            return {"error": exception, "message": "Ha ocurrido un error"}
        except Exception as e:
            logger.error(f"Error al obtener vista paciente. {e}")
            return {"error": e, "message": "Error, reintente luego"}


async def get_pdf_file_paciente(id_paciente: UUID, id_vacuna: UUID) -> httpx.Response | None:
    if id_paciente and id_vacuna:
        async with httpx.AsyncClient(base_url=BASE_URL) as client:
            try:
                params = {"idVacuna": str(id_vacuna), "idPaciente": str(id_paciente)}
                response = await client.get("/pdf", params=params)
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


def get_pdf_paciente_url(id_paciente: UUID, id_vacuna: UUID) -> str:
    return BASE_URL + f"/pdf?idVacuna={id_vacuna}&idPaciente={id_paciente}"
