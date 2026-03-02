from app.core.errors import UpstreamServiceError
from app.services.nac.client import get_nac_client


class DeviceSwapService:
    def __init__(self) -> None:
        self.client = get_nac_client()

    def get_swap_date(self, phone_number: str):
        try:
            my_device = self.client.devices.get(phone_number=phone_number)
            return my_device.get_device_swap_date()
        except Exception as exc:  # noqa: BLE001
            raise UpstreamServiceError(f"Device Swap date upstream error: {exc}") from exc

    def check_swap(self, phone_number: str, max_age_hours: int | None = None) -> bool:
        try:
            my_device = self.client.devices.get(phone_number=phone_number)
            if max_age_hours is None:
                return bool(my_device.verify_device_swap())
            return bool(my_device.verify_device_swap(max_age=max_age_hours))
        except Exception as exc:  # noqa: BLE001
            raise UpstreamServiceError(f"Device Swap check upstream error: {exc}") from exc
