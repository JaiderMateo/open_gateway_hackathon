from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class GeofenceCenter(BaseModel):
    latitude: float
    longitude: float


class GeofenceArea(BaseModel):
    area_type: Literal["CIRCLE", "POI"] = Field(alias="areaType")
    center: GeofenceCenter | None = None
    radius: int | None = None


class GeofenceDevice(BaseModel):
    phone_number: str | None = Field(default=None, pattern=r"^\+[1-9]\d{4,14}$", alias="phoneNumber")


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

    protocol: Literal["HTTP", "MQTT3", "MQTT5", "AMQP", "NATS", "KAFKA"]
    sink: str
    sink_credential: dict[str, Any] | None = Field(default=None, alias="sinkCredential")
    types: list[Literal["org.camaraproject.geofencing-subscriptions.v0.area-left", "org.camaraproject.geofencing-subscriptions.v0.area-entered"]] = Field(min_items=1, max_items=1)
    config: GeofenceConfig


class GeofenceSubscriptionResponse(BaseModel):
    protocol: Literal["HTTP"]
    sink: HttpUrl
    types: list[Literal["org.camaraproject.geofencing-subscriptions.v0.area-left", "org.camaraproject.geofencing-subscriptions.v0.area-entered"]]
    config: GeofenceConfig
    id: str
    starts_at: str = Field(alias="startsAt")


class GeofenceSubscriptionListResponse(BaseModel):
    subscriptions: list[GeofenceSubscriptionResponse]


class GeofenceSubscriptionDeleteResponse(BaseModel):
    status: str = "deleted"
    subscription_id: str = Field(alias="subscriptionId")
