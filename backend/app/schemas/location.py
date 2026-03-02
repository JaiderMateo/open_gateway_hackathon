from pydantic import BaseModel, ConfigDict, Field


class LocationVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")
    declared_lat: float = Field(ge=-90, le=90)
    declared_lon: float = Field(ge=-180, le=180)
    radius_m: float = Field(gt=0)


class LocationVerifyResponse(BaseModel):
    phone_number: str
    declared_lat: float
    declared_lon: float
    radius_m: float
    verified: bool | None
    message: str
