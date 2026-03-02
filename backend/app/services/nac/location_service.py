import json
from typing import Any

import requests

from app.core.config import get_settings
from app.core.errors import UpstreamServiceError


class LocationService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.rapidapi_key
        self.base_url = settings.rapidapi_base_url
        self.api_path = "/location-verification/v1"
        self.default_phone_number = settings.default_phone_number
        self.default_latitude = settings.default_latitude
        self.default_longitude = settings.default_longitude
        self.default_radius_m = settings.default_radius_m
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            url = f"{self.base_url}{self.api_path}/{endpoint}"
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"Location API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"Location service error: {exc}") from exc

    def verify_location(
        self,
        phone_number: str = None,
        declared_lat: float = None,
        declared_lon: float = None,
        radius_m: int = None,
    ) -> dict[str, Any]:
        """Verify device location with defaults from environment"""
        # Use defaults if parameters not provided
        phone_number = phone_number or self.default_phone_number
        declared_lat = declared_lat or self.default_latitude
        declared_lon = declared_lon or self.default_longitude
        radius_m = radius_m or self.default_radius_m
        
        payload = {
            "device": {"phoneNumber": phone_number},
            "area": {
                "areaType": "CIRCLE",
                "center": {
                    "latitude": declared_lat,
                    "longitude": declared_lon
                },
                "radius": radius_m
            }
        }
        return self._make_request("verify", payload)

    def retrieve_location(self, phone_number: str = None, max_age: int = 60) -> dict[str, Any]:
        """Retrieve device location"""
        phone_number = phone_number or self.default_phone_number
        
        payload = {
            "device": {"phoneNumber": phone_number},
            "maxAge": max_age
        }
        
        try:
            url = f"{self.base_url}/location-retrieval/v0/retrieve"
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"Location Retrieval API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"Location Retrieval service error: {exc}") from exc
