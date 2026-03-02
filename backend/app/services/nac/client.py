from functools import lru_cache

import network_as_code as nac

from app.core.config import get_settings


@lru_cache
def get_nac_client() -> nac.NetworkAsCodeClient:
    settings = get_settings()
    return nac.NetworkAsCodeClient(token=settings.nac_token)
