__all__ = (
    "auth_router",
    "user_settings_router",
)

from api.api_v1.routes.auth import router as auth_router
from api.api_v1.routes.user_settings import router as user_settings_router