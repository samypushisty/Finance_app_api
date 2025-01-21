from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource
from api.api_v1.services.environment_settings.currencies.service import UserCurrenciesService, UserCurrenciesServiceI
from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories import UserCategoriesServiceI, UserCategoriesService
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts import UserCashAccountsService,UserCashAccountsServiceI
from api.api_v1.services.user_settings.service import UserSettingsService
from api.api_v1.utils.repository import SQLAlchemyRepository
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from api.api_v1.services.auth.interface import AuthServiceI
from api.api_v1.services.auth.service import AuthService
from core.models.base import Category, CashAccount, Settings, User
from core.models.db_helper import DatabaseHelper
from core.redis_db.redis_helper import redis_session_getter

class DependencyContainer(containers.DeclarativeContainer):

    database_helper: Singleton["DatabaseHelper"] = Singleton(
        DatabaseHelper,
        url=str(settings.db.url),
        echo=settings.db.echo,
        echo_pool=settings.db.echo_pool,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )
    database_session: Resource["AsyncGenerator[AsyncSession, None]"] = Resource(database_helper.provided.session_getter)
    categories_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        session = database_session,
        model = Category,
    )
    cash_account_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        session = database_session,
        model = CashAccount,
    )
    settings_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        session = database_session,
        model = Settings,
    )
    user_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        session = database_session,
        model = User,
    )

    auth_service: Factory["AuthServiceI"] = Factory(AuthService, repository_user=user_repository, repository_settings=settings_repository)
    user_settings_service: Factory["UserSettingsServiceI"] = Factory(UserSettingsService,
                                                                     repository=settings_repository)
    user_categories_service: Factory["UserCategoriesServiceI"] = Factory(UserCategoriesService,
                                                                         repository=categories_repository)
    user_cash_accounts_service: Factory["UserCashAccountsServiceI"] = Factory(UserCashAccountsService,
                                                                              repository=cash_account_repository)
    user_currency_service: Factory["UserCurrenciesServiceI"] = Factory(UserCurrenciesService,
                                                                              db_redis=redis_session_getter)

container = DependencyContainer()