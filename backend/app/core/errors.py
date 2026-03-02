from fastapi import HTTPException


class UpstreamServiceError(HTTPException):
    def __init__(self, detail: str = "Upstream service error") -> None:
        super().__init__(status_code=502, detail=detail)


class NotImplementedAPIError(HTTPException):
    def __init__(self, detail: str = "Capability not implemented yet") -> None:
        super().__init__(status_code=501, detail=detail)
