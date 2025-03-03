__all__ = (
    "auth_router",
    "user_settings_router",
    "user_categories_router",
    "user_cash_accounts_router",
    "type_of_earnings_router",
    "currency_router",
    "movies_router",
    "total_balance_router"
)

from api.api_v1.routes.auth import router as auth_router
from api.api_v1.routes.user_settings import router as user_settings_router
from api.api_v1.routes.user_categories import router as user_categories_router
from api.api_v1.routes.cash_accounts import router as user_cash_accounts_router
from api.api_v1.routes.currencies import router as currency_router
from api.api_v1.routes.type_of_earnings import router as type_of_earnings_router
from api.api_v1.routes.movies import router as movies_router
from api.api_v1.routes.total_balance import router as total_balance_router
