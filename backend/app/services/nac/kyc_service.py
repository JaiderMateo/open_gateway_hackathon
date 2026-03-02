import json
import uuid
from typing import Any

import requests

from app.core.config import get_settings
from app.core.errors import UpstreamServiceError


class KycService:
    def __init__(self) -> None:
        settings = get_settings()
        self.api_key = settings.rapidapi_key
        self.base_url = settings.rapidapi_base_url
        self.api_base_path = "/passthrough/camara/v1"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "network-as-code.nokia.rapidapi.com",
            "Content-Type": "application/json",
        }

    def _make_request(
        self,
        endpoint: str,
        payload: dict[str, Any] | None = None,
        method: str = "POST",
    ) -> dict[str, Any]:
        try:
            url = f"{self.base_url}{self.api_base_path}/{endpoint}"
            
            if method.upper() == "POST":
                response = requests.post(url, json=payload, headers=self.headers)
            else:
                response = requests.get(url, headers=self.headers)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"KYC API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"KYC service error: {exc}") from exc

    def fill_in(self, phone_number: str) -> dict[str, Any]:
        """Fill in KYC customer information"""
        payload = {"phoneNumber": phone_number}
        return self._make_request("kyc-fill-in/kyc-fill-in/v0.4/fill-in", payload)

    def match(self, phone_number: str) -> dict[str, Any]:
        """Verify KYC match"""
        payload = {
            "phoneNumber": phone_number,
            "idDocument": "66666666q",
            "name": "Federica Sanchez Arjona",
            "givenName": "Federica",
            "familyName": "Sanchez Arjona",
            "nameKanaHankaku": "federica",
            "nameKanaZenkaku": "Ｆｅｄｅｒｉｃａ",
            "middleNames": "Sanchez",
            "familyNameAtBirth": "YYYY",
            "address": "Tokyo-to Chiyoda-ku Iidabashi 3-10-10",
            "streetName": "Nicolas Salmeron",
            "streetNumber": "4",
            "postalCode": "1028460",
            "region": "Tokyo",
            "locality": "ZZZZ",
            "country": "JP",
            "houseNumberExtension": "VVVV",
            "birthdate": "1978-08-22",
            "email": "abc@example.com",
            "gender": "OTHER"
        }
        headers = self.headers.copy()
        headers["x-correlator"] = str(uuid.uuid4())
        
        try:
            url = f"{self.base_url}{self.api_base_path}/kyc-match/kyc-match/v0.3/match"
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"KYC Match API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"KYC Match service error: {exc}") from exc

    def tenure(self, phone_number: str) -> dict[str, Any]:
        """Check KYC tenure"""
        payload = {
            "phoneNumber": phone_number,
            "tenureDate": "2023-07-03"
        }
        headers = self.headers.copy()
        headers["x-correlator"] = str(uuid.uuid4())
        
        try:
            url = f"{self.base_url}{self.api_base_path}/kyc-tenure/kyc-tenure/v0.1/check-tenure"
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            raise UpstreamServiceError(f"KYC Tenure API error: {exc}") from exc
        except Exception as exc:
            raise UpstreamServiceError(f"KYC Tenure service error: {exc}") from exc
