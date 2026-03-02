from fastapi import APIRouter

from app.core.config import get_settings
from app.schemas.device_swap import (
    DeviceSwapCheckRequest,
    DeviceSwapCheckResponse,
    DeviceSwapDateRequest,
    DeviceSwapDateResponse,
)
from app.schemas.health import HealthResponse
from app.schemas.geofence import (
    GeofenceSubscriptionDeleteResponse,
    GeofenceSubscriptionListResponse,
    GeofenceSubscriptionRequest,
    GeofenceSubscriptionResponse,
)
from app.schemas.kyc import (
    KycFillInRequest,
    KycFillInResponse,
    KycMatchRequest,
    KycTenureRequest,
)
from app.schemas.location import LocationVerifyRequest, LocationVerifyResponse
from app.schemas.sim_swap import (
    SimSwapCheckRequest,
    SimSwapCheckResponse,
    SimSwapDateRequest,
    SimSwapDateResponse,
)
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


@router.post("/nac/device-swap/date", response_model=DeviceSwapDateResponse)
def device_swap_date(payload: DeviceSwapDateRequest) -> DeviceSwapDateResponse:
    swap_date = device_swap_service.get_swap_date(payload.phone_number)
    return DeviceSwapDateResponse(
        phone_number=payload.phone_number,
        device_swap_date=swap_date,
    )


@router.post("/nac/device-swap/check", response_model=DeviceSwapCheckResponse)
def device_swap_check(payload: DeviceSwapCheckRequest) -> DeviceSwapCheckResponse:
    swapped = device_swap_service.check_swap(
        phone_number=payload.phone_number,
        max_age_hours=payload.max_age_hours,
    )
    return DeviceSwapCheckResponse(
        phone_number=payload.phone_number,
        max_age_hours=payload.max_age_hours,
        swapped_recently=swapped,
    )


@router.post("/nac/sim-swap/date", response_model=SimSwapDateResponse)
def sim_swap_date(payload: SimSwapDateRequest) -> SimSwapDateResponse:
    swap_date = sim_swap_service.get_swap_date(payload.phone_number)
    return SimSwapDateResponse(phone_number=payload.phone_number, sim_swap_date=swap_date)


@router.post("/nac/sim-swap/check", response_model=SimSwapCheckResponse)
def sim_swap_check(payload: SimSwapCheckRequest) -> SimSwapCheckResponse:
    swapped = sim_swap_service.check_swap(payload.phone_number, payload.max_age_hours)
    return SimSwapCheckResponse(
        phone_number=payload.phone_number,
        max_age_hours=payload.max_age_hours,
        swapped_recently=swapped,
    )


@router.post("/nac/kyc/fill-in", response_model=KycFillInResponse)
def kyc_fill_in(payload: KycFillInRequest) -> KycFillInResponse:
    customer_info = kyc_service.fill_in(payload.phone_number)
    return KycFillInResponse(phone_number=payload.phone_number, customer_info=customer_info)


@router.post("/nac/kyc/match")
def kyc_match(payload: KycMatchRequest) -> dict[str, str]:
    kyc_service.match(payload.phone_number)
    return {"status": "ok"}


@router.post("/nac/kyc/tenure")
def kyc_tenure(payload: KycTenureRequest) -> dict[str, str]:
    kyc_service.tenure(payload.phone_number)
    return {"status": "ok"}


@router.post("/nac/location/verify", response_model=LocationVerifyResponse)
def location_verify(payload: LocationVerifyRequest) -> LocationVerifyResponse:
    verified = location_service.verify_location(
        phone_number=payload.phone_number,
        declared_lat=payload.declared_lat,
        declared_lon=payload.declared_lon,
        radius_m=payload.radius_m,
    )
    return LocationVerifyResponse(
        phone_number=payload.phone_number,
        declared_lat=payload.declared_lat,
        declared_lon=payload.declared_lon,
        radius_m=payload.radius_m,
        verified=verified,
        message="Location verification result",
    )


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
