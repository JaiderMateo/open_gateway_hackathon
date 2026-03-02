from typing import Any

from app.core.errors import NotImplementedAPIError, UpstreamServiceError
from app.services.nac.client import get_nac_client


class KycService:
    def __init__(self) -> None:
        self.client = get_nac_client()

    def fill_in(self, phone_number: str) -> dict[str, Any]:
        try:
            data = self.client.kyc.request_customer_info(phone_number=phone_number)
            if hasattr(data, "model_dump"):
                return data.model_dump()  # type: ignore[no-any-return]
            if isinstance(data, dict):
                return data
            return {"raw": str(data)}
        except Exception as exc:  # noqa: BLE001
            raise UpstreamServiceError(f"KYC Fill-in upstream error: {exc}") from exc

    def match(self, phone_number: str) -> None:
        raise NotImplementedAPIError(
            "TODO: Implement KYC Match once SDK method is confirmed for this account/product scope"
        )

    def tenure(self, phone_number: str) -> None:
        raise NotImplementedAPIError(
            "TODO: Implement KYC Tenure once SDK method is confirmed for this account/product scope"
        )
