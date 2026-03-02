import json
from typing import Any

import requests

from app.core.config import get_settings
from app.core.errors import UpstreamServiceError


class GeofenceService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.rapidapi_key
        self.base_url = "https://network-as-code.p-eu.rapidapi.com/geofencing-subscriptions/v0.3"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, headers=self.headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, json=payload, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"Geofence API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"Geofence service error: {exc}") from exc

    def get_subscription_list(self) -> dict[str, Any]:
        """Retrieve all geofencing subscriptions"""
        return self._make_request("GET", "/subscriptions")

    def create_subscription(self, subscription_data: dict[str, Any]) -> dict[str, Any]:
        """Create a new geofencing subscription"""
        return self._make_request("POST", "/subscriptions", subscription_data)

    def get_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Retrieve a specific geofencing subscription"""
        return self._make_request("GET", f"/subscriptions/{subscription_id}")

    def delete_subscription(self, subscription_id: str) -> dict[str, Any]:
        """Delete a geofencing subscription"""
        return self._make_request("DELETE", f"/subscriptions/{subscription_id}", {})
