from typing import Any

from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.device_swap import DeviceSwapCheckRequest, DeviceSwapDateRequest
from app.schemas.health import HealthResponse
from app.schemas.geofence import (
    GeofenceSubscriptionDeleteResponse,
    GeofenceSubscriptionListResponse,
    GeofenceSubscriptionRequest,
    GeofenceSubscriptionResponse,
)
from app.schemas.kyc import KycFillInRequest, KycMatchRequest, KycTenureRequest
from app.schemas.location import LocationVerifyRequest, LocationVerifyResponse
from app.schemas.location_retrieve import LocationRetrieveRequest
from app.schemas.sim_swap import SimSwapCheckRequest, SimSwapDateRequest
from app.services.nac.device_swap_service import DeviceSwapService
from app.services.nac.geofence_service import GeofenceService
from app.services.nac.kyc_service import KycService
from app.services.nac.location_service import LocationService
from app.services.nac.sim_swap_service import SimSwapService

router = APIRouter()
device_swap_service = DeviceSwapService()
sim_swap_service = SimSwapService()
kyc_service = KycService()
location_service = LocationService()
geofence_service = GeofenceService()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", env=settings.app_env)


@router.post("/nac/device-swap/date")
def device_swap_date(payload: DeviceSwapDateRequest) -> dict[str, Any]:
    swap_date = device_swap_service.get_swap_date(payload.phone_number)
    return swap_date


@router.post("/nac/device-swap/check")
def device_swap_check(payload: DeviceSwapCheckRequest) -> dict[str, Any]:
    swapped = device_swap_service.check_swap(
        phone_number=payload.phone_number,
        max_age_hours=payload.max_age_hours,
    )
    return swapped


@router.post("/nac/sim-swap/date")
def sim_swap_date(payload: SimSwapDateRequest) -> dict[str, Any]:
    swap_date = sim_swap_service.get_swap_date(payload.phone_number)
    return swap_date


@router.post("/nac/sim-swap/check")
def sim_swap_check(payload: SimSwapCheckRequest) -> dict[str, Any]:
    swapped = sim_swap_service.check_swap(payload.phone_number, payload.max_age_hours)
    return swapped


@router.post("/nac/kyc/fill-in")
def kyc_fill_in(payload: KycFillInRequest) -> dict[str, Any]:
    customer_info = kyc_service.fill_in(payload.phone_number)
    return customer_info


@router.post("/nac/kyc/match")
def kyc_match(payload: KycMatchRequest) -> dict[str, Any]:
    match_result = kyc_service.match(payload.phone_number)
    return match_result


@router.post("/nac/kyc/tenure")
def kyc_tenure(payload: KycTenureRequest) -> dict[str, Any]:
    tenure_result = kyc_service.tenure(payload.phone_number)
    return tenure_result


@router.post("/nac/location/verify")
def location_verify(payload: LocationVerifyRequest) -> dict[str, Any]:
    verified = location_service.verify_location(
        phone_number=payload.phone_number,
        declared_lat=payload.declared_lat,
        declared_lon=payload.declared_lon,
        radius_m=payload.radius_m,
    )
    return verified


@router.post("/nac/location/verify-defaults")
def location_verify_defaults() -> dict[str, Any]:
    """Verify location using default parameters from environment"""
    verified = location_service.verify_location()
    return verified


@router.post("/nac/location/retrieve")
def location_retrieve(payload: LocationRetrieveRequest) -> dict[str, Any]:
    """Retrieve device location"""
    location_data = location_service.retrieve_location(payload.phone_number, payload.max_age)
    return location_data


@router.post("/nac/location/retrieve-defaults")
def location_retrieve_defaults() -> dict[str, Any]:
    """Retrieve device location using default phone number"""
    location_data = location_service.retrieve_location()
    return location_data


@router.get("/nac/geofence/subscriptions", response_model=GeofenceSubscriptionListResponse)
def get_geofence_subscriptions() -> GeofenceSubscriptionListResponse:
    """Retrieve all geofencing subscriptions"""
    subscriptions_data = geofence_service.get_subscription_list()
    return GeofenceSubscriptionListResponse(subscriptions=subscriptions_data)


@router.post("/nac/geofence/subscriptions", response_model=GeofenceSubscriptionResponse)
def create_geofence_subscription(payload: GeofenceSubscriptionRequest) -> GeofenceSubscriptionResponse:
    """Create a new geofencing subscription"""
    subscription_data = geofence_service.create_subscription(payload.model_dump(by_alias=True))
    return GeofenceSubscriptionResponse(**subscription_data)


@router.get("/nac/geofence/subscriptions/{subscription_id}", response_model=GeofenceSubscriptionResponse)
def get_geofence_subscription(subscription_id: str) -> GeofenceSubscriptionResponse:
    """Retrieve a specific geofencing subscription"""
    subscription_data = geofence_service.get_subscription(subscription_id)
    return GeofenceSubscriptionResponse(**subscription_data)


@router.delete("/nac/geofence/subscriptions/{subscription_id}", response_model=GeofenceSubscriptionDeleteResponse)
def delete_geofence_subscription(subscription_id: str) -> GeofenceSubscriptionDeleteResponse:
    """Delete a geofencing subscription"""
    geofence_service.delete_subscription(subscription_id)
    return GeofenceSubscriptionDeleteResponse(subscriptionId=subscription_id)
