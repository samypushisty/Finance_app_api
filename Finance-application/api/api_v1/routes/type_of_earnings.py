from fastapi import APIRouter, Depends
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.environment_settings.CRUD_user_earnings import UserEarningsServiceI
from api.api_v1.services.environment_settings.CRUD_user_earnings.schemas import UserTypeEarningsGet, \
    UserTypeEarningsRead, UserTypesEarningsRead, UserTypeEarningsPatch, UserTypeEarningsPost
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(prefix="/type_of_earnings", tags=["EnvironmentSettings"])

async def get_user_type_of_earnings_service() -> UserEarningsServiceI:
    return container.user_type_of_earnings_service()

@router.post("")
async def post_type_earnings(
        user_type_of_earnings: UserTypeEarningsPost,
        token: JwtInfo = Depends(validation),
        user_type_of_earnings_service = Depends(get_user_type_of_earnings_service),
        ):
    await user_type_of_earnings_service.post_user_type_of_earnings(user_type_of_earnings=user_type_of_earnings,token=token)


@router.patch("")
async def patch_type_earnings(
        user_type_of_earnings: UserTypeEarningsPatch,
        token: JwtInfo = Depends(validation),
        user_type_of_earnings_service = Depends(get_user_type_of_earnings_service),
        ):
    await user_type_of_earnings_service.patch_type_of_earnings(user_type_of_earnings=user_type_of_earnings,token=token)

@router.get("/all",response_model=GenericResponse[UserTypesEarningsRead])
async def get_types_earnings(
        token: JwtInfo = Depends(validation),
        user_type_of_earnings_service = Depends(get_user_type_of_earnings_service),
        ):
    return await user_type_of_earnings_service.get_types_of_earnings(token=token)


@router.get("",response_model=GenericResponse[UserTypeEarningsRead])
async def get_type_earnings(
        user_type_of_earnings: UserTypeEarningsGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_type_of_earnings_service = Depends(get_user_type_of_earnings_service),
        ):
    return await user_type_of_earnings_service.get_type_of_earnings(user_type_of_earnings=user_type_of_earnings, token=token)

@router.delete("")
async def delete_type_earnings(
        user_type_of_earnings: UserTypeEarningsGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_type_of_earnings_service = Depends(get_user_type_of_earnings_service),
        ):
    await user_type_of_earnings_service.delete_type_of_earnings(user_type_of_earnings=user_type_of_earnings,token=token)
