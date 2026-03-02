from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class KycFillInRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")


class KycFillInResponse(BaseModel):
    phone_number: str
    customer_info: dict[str, Any]


class KycMatchRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")


class KycTenureRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
