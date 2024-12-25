from fastapi import APIRouter, Depends
from api.api_v1.container import container
from api.api_v1.services.auth.interface import AuthServiceI
from api.api_v1.services.auth.schemas import UserAuth, JWTRead
from api.api_v1.services.base_schemas.schemas import GenericResponse

router = APIRouter(tags=["Auth"])

async def get_auth_service() -> AuthServiceI:
    return container.auth_service()

@router.post("",response_model=GenericResponse[JWTRead])
async def get_users(
        user: UserAuth,
        auth_service = Depends(get_auth_service),
        ):
    return await auth_service.get_user(user=user)

