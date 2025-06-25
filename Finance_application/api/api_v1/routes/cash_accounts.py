from fastapi import APIRouter, Depends
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts import UserCashAccountsServiceI
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.environment_settings.CRUD_user_cash_accounts.schemas import UserCashAccountPost, \
    UserCashAccountPatch, UserCashAccountsRead, UserCashAccountRead, UserCashAccountGet, UserCashAccountDelete
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(prefix="/cash_accounts", tags=["EnvironmentSettings"])


async def get_user_cash_accounts_service() -> UserCashAccountsServiceI:
    return container.user_cash_accounts_service()

@router.post("")
async def post_category(
        user_cash_account: UserCashAccountPost,
        token: JwtInfo = Depends(validation),
        user_cash_account_service = Depends(get_user_cash_accounts_service),
        ):
    await user_cash_account_service.post_user_cash_account(user_cash_account=user_cash_account,token=token)


@router.patch("")
async def patch_category(
        user_cash_account: UserCashAccountPatch,
        token: JwtInfo = Depends(validation),
        user_cash_account_service = Depends(get_user_cash_accounts_service),
        ):
    await user_cash_account_service.patch_user_cash_account(user_cash_account=user_cash_account,token=token)

@router.get("/all",response_model=GenericResponse[UserCashAccountsRead])
async def get_categories(
        token: JwtInfo = Depends(validation),
        user_cash_account_service = Depends(get_user_cash_accounts_service),
        ):
    return await user_cash_account_service.get_user_cash_accounts(token=token)


@router.get("",response_model=GenericResponse[UserCashAccountRead])
async def get_category(
        user_cash_account: UserCashAccountGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_cash_account_service = Depends(get_user_cash_accounts_service),
        ):
    return await user_cash_account_service.get_user_cash_account(user_cash_account=user_cash_account, token=token)

@router.delete("")
async def delete_category(
        user_cash_account: UserCashAccountDelete = Depends(),
        token: JwtInfo = Depends(validation),
        user_cash_account_service = Depends(get_user_cash_accounts_service),
        ):
    await user_cash_account_service.delete_user_cash_account(user_cash_account=user_cash_account,token=token)
