from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory, Resource

from api.api_v1.services.CRUD_Movie_on_account import UserMovieService,UserMovieServiceI
from api.api_v1.services.environment_settings.CRUD_user_earnings import UserEarningsService, UserEarningsServiceI
from api.api_v1.services.environment_settings.currencies import UserCurrenciesService, UserCurrenciesServiceI
from api.api_v1.services.total_balance import UserBalanceService, UserBalanceServiceI
from api.api_v1.services.user_settings import UserSettingsService, UserSettingsServiceI
from api.api_v1.services.environment_settings.CRUD_user_categories import UserCategoriesServiceI, UserCategoriesService
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts import UserCashAccountsService,UserCashAccountsServiceI
from api.api_v1.services.auth import AuthService, AuthServiceI

from api.api_v1.utils.work_with_money import WorkWithMoneyRepository
from api.api_v1.utils.repository import SQLAlchemyRepository
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from core.models.base import Category, CashAccount, UserSettings, User, Earnings, MovieOnAccount, Balance
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
        model = Category,
    )
    cash_account_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model = CashAccount,
    )
    settings_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model = UserSettings,
    )
    user_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model = User,
    )
    type_of_earnings_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=Earnings,
    )
    movies_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=MovieOnAccount,
    )

    balance_repository: Singleton["SQLAlchemyRepository"] = Singleton(
        SQLAlchemyRepository,
        model=Balance,
    )

    work_with_money_repository: Singleton["WorkWithMoneyRepository"] = Singleton(
        WorkWithMoneyRepository,
        db_redis=redis_session_getter,
        repository_cash_account=cash_account_repository,
        repository_balance=balance_repository,
        repository_categories=categories_repository,
        repository_type_of_earnings=type_of_earnings_repository
    )

    auth_service: Factory["AuthServiceI"] = Factory(AuthService,
                                                    repository_user=user_repository,
                                                    repository_settings=settings_repository,
                                                    repository_balance=balance_repository,
                                                    database_session=database_session)
    user_settings_service: Factory["UserSettingsServiceI"] = Factory(UserSettingsService,
                                                                     repository=settings_repository,
                                                                     database_session=database_session)
    user_categories_service: Factory["UserCategoriesServiceI"] = Factory(UserCategoriesService,
                                                                         work_with_money=work_with_money_repository,
                                                                         repository=categories_repository,
                                                                         database_session=database_session,
                                                                         movies_repository=movies_repository,
                                                                         balance_repository=balance_repository,
                                                                         cash_account_repository=cash_account_repository)
    user_cash_accounts_service: Factory["UserCashAccountsServiceI"] = Factory(UserCashAccountsService,
                                                                              work_with_money=work_with_money_repository,
                                                                              repository=cash_account_repository,
                                                                              database_session=database_session,
                                                                              repository_movies=movies_repository)
    user_type_of_earnings_service: Factory["UserEarningsServiceI"] = Factory(UserEarningsService,
                                                                             work_with_money=work_with_money_repository,
                                                                             repository=type_of_earnings_repository,
                                                                             database_session=database_session,
                                                                             repository_movies=movies_repository)
    user_currency_service: Factory["UserCurrenciesServiceI"] = Factory(UserCurrenciesService,
                                                                       db_redis=redis_session_getter,
                                                                       database_session=database_session)
    user_movies_service: Factory["UserMovieServiceI"] = Factory(UserMovieService,
                                                                work_with_money = work_with_money_repository,
                                                                repository=movies_repository,
                                                                database_session=database_session
                                                                )
    user_total_balance_service: Factory["UserBalanceServiceI"] = Factory(UserBalanceService,
                                                                         db_redis=redis_session_getter,
                                                                         work_with_money=work_with_money_repository,
                                                                         database_session=database_session,
                                                                         repository_balance=balance_repository,
                                                                         settings_repository=settings_repository
                                                                         )

container = DependencyContainer()