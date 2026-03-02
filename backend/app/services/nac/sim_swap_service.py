from app.core.errors import NotImplementedAPIError


class SimSwapService:
    def get_swap_date(self, phone_number: str):
        raise NotImplementedAPIError(
            "TODO: SIM Swap date method not mapped yet in SDK docs. Implement once exact method is validated."
        )

    def check_swap(self, phone_number: str, max_age_hours: int | None = None) -> bool:
        raise NotImplementedAPIError(
            "TODO: SIM Swap check method not mapped yet in SDK docs. Implement once exact method is validated."
        )
