from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource
from api.api_v1.services.user_settings.interface import UserSettingsServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories import UserCategoriesServiceI, UserCategoriesService
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts import UserCashAccountsService,UserCashAccountsServiceI
from api.api_v1.services.user_settings.service import UserSettingsService
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from api.api_v1.services.auth.interface import AuthServiceI
from api.api_v1.services.auth.service import AuthService
from core.models.db_helper import DatabaseHelper


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

    auth_service: Factory["AuthServiceI"] = Factory(AuthService, session=database_session)
    user_settings_service: Factory["UserSettingsServiceI"] = Factory(UserSettingsService, session=database_session)
    user_categories_service: Factory["UserCategoriesServiceI"] = Factory(UserCategoriesService, session=database_session)
    user_cash_accounts_service: Factory["UserCashAccountsServiceI"] = Factory(UserCashAccountsService,session=database_session)

container = DependencyContainer()