from fastapi import APIRouter, Depends

from api.api_v1.services.environment_settings.currencies import UserCurrenciesServiceI
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.environment_settings.currencies.schemas import CurrencyRead, CurrenciesRead, CurrencyGet
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(prefix="/currencies",tags=["Currencies"])

async def get_currencies_service() -> UserCurrenciesServiceI:
    return container.user_currency_service()


@router.get("",response_model=GenericResponse[CurrencyRead])
async def get_currency_price(
        name_currency: CurrencyGet  = Depends(),
        token: JwtInfo = Depends(validation),
        currencies_service = Depends(get_currencies_service),

        ):
    return await currencies_service.get_currency_price(name_currency=name_currency)


@router.get("/all",response_model=GenericResponse[CurrenciesRead])
async def get_currencies(
        token: JwtInfo = Depends(validation),
        currencies_service = Depends(get_currencies_service),
        ):
    return await currencies_service.get_currencies()