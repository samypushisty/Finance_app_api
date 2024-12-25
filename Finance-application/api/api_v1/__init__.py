from fastapi import APIRouter

from core.config import settings

from .routes import auth_router
from .routes import user_settings_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    auth_router,
    prefix=settings.api.v1.auth,
)

router.include_router(
    user_settings_router,
    prefix=settings.api.v1.settings,
)