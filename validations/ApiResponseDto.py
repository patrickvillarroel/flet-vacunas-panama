from typing import List, Optional

from pydantic import BaseModel


class ApiFailedDto(BaseModel):
    code: Optional[str]
    property: Optional[str]
    message: Optional[str]


class ApiResponseDto(BaseModel):
    status: dict
    data: dict
    errors: List[ApiFailedDto]
    warnings: List[ApiFailedDto]
    metadata: dict
