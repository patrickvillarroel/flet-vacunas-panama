from pydantic import BaseModel
from typing import List


class ApiResponseDto(BaseModel):
    status: dict
    data: dict
    errors: List[dict]
    warnings: List[dict]
    metadata: dict
