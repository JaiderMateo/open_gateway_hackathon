from app.core.errors import NotImplementedAPIError


class LocationService:
    def verify_location(
        self,
        phone_number: str,
        declared_lat: float,
        declared_lon: float,
        radius_m: float,
    ) -> bool | None:
        raise NotImplementedAPIError(
            "TODO: Implement Location Verification when exact SDK method is confirmed in available product scope."
        )
