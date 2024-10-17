import logging
import os
from typing import List, Set

import httpx
from dotenv import load_dotenv

from validations.ApiResponseDto import ApiResponseDto
from validations.DireccionesDto import DistritoDto, ProvinciaDto

logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="assets/.env")
BASE_URL = os.getenv("BASE_URL")
logger.info(f"BASE_URL: {BASE_URL}")


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
        except httpx.HTTPStatusError as execption:
            logger.error(execption)
            return []
        except Exception as e:
            logger.error(f"Error al obtener provincias. {e}")
            return []
