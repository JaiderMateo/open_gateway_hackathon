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
        phone_number: str,
        declared_lat: float,
        declared_lon: float,
        radius_m: float,
    ) -> dict[str, Any]:
        """Verify device location"""
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
