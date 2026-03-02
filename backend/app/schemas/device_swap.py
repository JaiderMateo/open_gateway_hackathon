from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DeviceSwapDateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")


class DeviceSwapDateResponse(BaseModel):
    phone_number: str
    device_swap_date: datetime | None


class DeviceSwapCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    max_age_hours: int | None = Field(default=None, ge=1, le=2400)


class DeviceSwapCheckResponse(BaseModel):
    phone_number: str
    max_age_hours: int | None
    swapped_recently: bool
