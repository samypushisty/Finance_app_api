from fastapi import APIRouter, Depends
from api.api_v1.services.total_balance import UserBalanceService, UserBalanceServiceI
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.total_balance.schemas import BalancesHistoryRead, BalanceRead
from api.api_v1.services.user_settings.schemas import UserSettingsPatch, UserSettingsRead
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["TotalBalance"])

async def get_total_balance_service() -> UserBalanceServiceI:
    return container.user_total_balance_service()

@router.get("",response_model=GenericResponse[BalanceRead])
async def get_total_balance(
        token: JwtInfo = Depends(validation),
        total_balance_service: UserBalanceService = Depends(get_total_balance_service),
        ):
    return await total_balance_service.get_balance(token=token)


@router.get("/all",response_model=GenericResponse[BalancesHistoryRead])
async def get_history_balances(
        token: JwtInfo = Depends(validation),
        total_balance_service: UserBalanceService = Depends(get_total_balance_service),
        ):
    return await total_balance_service.get_balances(token=token)