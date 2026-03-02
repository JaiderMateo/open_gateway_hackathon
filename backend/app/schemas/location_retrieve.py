from pydantic import BaseModel, Field


class LocationRetrieveRequest(BaseModel):
    phone_number: str = Field(..., description="Phone number to retrieve location for")
    max_age: int = Field(default=60, description="Maximum age of location data in seconds")
