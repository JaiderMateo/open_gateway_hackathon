from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class GeofenceArea(BaseModel):
    area_type: Literal["CIRCLE"] = Field(alias="areaType")
    center: dict[str, float]
    radius: int


class GeofenceDevice(BaseModel):
    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$", alias="phoneNumber")


class GeofenceSubscriptionDetail(BaseModel):
    device: GeofenceDevice
    area: GeofenceArea


class GeofenceConfig(BaseModel):
    subscription_detail: GeofenceSubscriptionDetail = Field(alias="subscriptionDetail")
    initial_event: bool = Field(default=True, alias="initialEvent")
    subscription_max_events: int | None = Field(default=None, alias="subscriptionMaxEvents")
    subscription_expire_time: str | None = Field(default=None, alias="subscriptionExpireTime")


class GeofenceSubscriptionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    protocol: Literal["HTTP"]
    sink: HttpUrl
    types: list[Literal["org.camaraproject.geofencing-subscriptions.v0.area-entered"]]
    config: GeofenceConfig


class GeofenceSubscriptionResponse(BaseModel):
    protocol: Literal["HTTP"]
    sink: HttpUrl
    types: list[Literal["org.camaraproject.geofencing-subscriptions.v0.area-entered"]]
    config: GeofenceConfig
    id: str
    starts_at: str = Field(alias="startsAt")


class GeofenceSubscriptionListResponse(BaseModel):
    subscriptions: list[GeofenceSubscriptionResponse]


class GeofenceSubscriptionDeleteResponse(BaseModel):
    status: str = "deleted"
    subscription_id: str = Field(alias="subscriptionId")
