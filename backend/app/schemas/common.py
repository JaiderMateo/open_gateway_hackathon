from pydantic import BaseModel, ConfigDict, Field

PhoneNumberE164 = Field(pattern=r"^\+[1-9]\d{7,14}$")


class APIResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
