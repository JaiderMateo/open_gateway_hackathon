from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SimSwapDateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")


class SimSwapDateResponse(BaseModel):
    phone_number: str
    sim_swap_date: datetime | None


class SimSwapCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    max_age_hours: int | None = Field(default=None, ge=1, le=2400)


class SimSwapCheckResponse(BaseModel):
    phone_number: str
    max_age_hours: int | None
    swapped_recently: bool
