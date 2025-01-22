from fastapi import APIRouter

from core.config import settings

from api.api_v1.routes import (auth_router, user_categories_router,user_settings_router,user_cash_accounts_router,
                               currency_router, type_of_earnings_router)


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

router.include_router(
    user_categories_router,
    prefix=settings.api.v1.environment_settings,
)

router.include_router(
    user_cash_accounts_router,
    prefix=settings.api.v1.environment_settings,
)

router.include_router(
    currency_router,
    prefix=settings.api.v1.environment_settings,
)

router.include_router(
    type_of_earnings_router,
    prefix=settings.api.v1.environment_settings,
)