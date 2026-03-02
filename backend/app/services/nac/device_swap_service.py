import json
from typing import Any

import requests

from app.core.config import get_settings
from app.core.errors import UpstreamServiceError


class DeviceSwapService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.rapidapi_key
        self.base_url = settings.rapidapi_base_url
        self.api_path = "/passthrough/camara/v1/device-swap/device-swap/v1"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            url = f"{self.base_url}{self.api_path}/{endpoint}"
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"Device Swap API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"Device Swap service error: {exc}") from exc

    def get_swap_date(self, phone_number: str) -> dict[str, Any]:
        """Retrieve device swap date"""
        payload = {"phoneNumber": phone_number}
        return self._make_request("retrieve-date", payload)

    def check_swap(self, phone_number: str, max_age_hours: int | None = None) -> dict[str, Any]:
        """Check if device was swapped recently"""
        payload = {"phoneNumber": phone_number}
        if max_age_hours is not None:
            payload["maxAgeHours"] = max_age_hours
        return self._make_request("check", payload)
