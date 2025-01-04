from fastapi import APIRouter, Depends
from api.api_v1.services.environment_settings.CRUD_user_categories import UserCategoriesServiceI
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from api.api_v1.services.environment_settings.CRUD_user_categories.schemas import UserCategoryPost, UserCategoriesRead, \
    UserCategoryPatch, UserCategoryGet, UserCategoryRead
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(prefix="/category", tags=["EnvironmentSettings"])

async def get_user_categories_service() -> UserCategoriesServiceI:
    return container.user_categories_service()

@router.post("")
async def post_category(
        user_category: UserCategoryPost,
        token: JwtInfo = Depends(validation),
        user_category_service = Depends(get_user_categories_service),
        ):
    await user_category_service.post_user_category(user_category=user_category,token=token)


@router.patch("")
async def patch_category(
        user_category: UserCategoryPatch,
        token: JwtInfo = Depends(validation),
        user_category_service = Depends(get_user_categories_service),
        ):
    await user_category_service.patch_user_category(user_category=user_category,token=token)

@router.get("/all",response_model=GenericResponse[UserCategoriesRead])
async def get_categories(
        token: JwtInfo = Depends(validation),
        user_category_service = Depends(get_user_categories_service),
        ):
    return await user_category_service.get_user_categories(token=token)


@router.get("",response_model=GenericResponse[UserCategoryRead])
async def get_category(
        user_category: UserCategoryGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_category_service = Depends(get_user_categories_service),
        ):
    return await user_category_service.get_user_category(user_category=user_category, token=token)

@router.delete("")
async def delete_category(
        user_category: UserCategoryGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_category_service = Depends(get_user_categories_service),
        ):
    await user_category_service.delete_user_category(user_category=user_category,token=token)
