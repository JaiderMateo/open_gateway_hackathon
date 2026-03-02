from app.schemas.common import APIResponse


class HealthResponse(APIResponse):
    status: str
    env: str
