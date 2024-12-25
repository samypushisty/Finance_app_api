__all__ = (
    "auth_router",
    "user_settings_router",
)

from .auth import router as auth_router
from .user_settings import router as user_settings_router