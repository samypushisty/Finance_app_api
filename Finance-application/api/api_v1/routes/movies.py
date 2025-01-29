from fastapi import APIRouter, Depends

from api.api_v1.services.CRUD_Movie_on_account.interface import UserMovieServiceI
from api.api_v1.services.CRUD_Movie_on_account.schemas import UserMoviePost, UserMovieGet, UserMovieRead, \
    UserMoviesRead, UserMoviePatch
from api.api_v1.container import container
from api.api_v1.services.base_schemas.schemas import GenericResponse
from secure import JwtInfo
from secure.jwt_functions import validation

router = APIRouter(tags=["Money movies"])

async def get_movies_service() -> UserMovieServiceI:
    return container.user_movies_service()

@router.post("")
async def post_movie(
        user_movie: UserMoviePost,
        token: JwtInfo = Depends(validation),
        user_movies_service = Depends(get_movies_service),
        ):
    await user_movies_service.post_movie(user_movie=user_movie,token=token)


@router.patch("")
async def patch_movie(
        user_movie: UserMoviePatch,
        token: JwtInfo = Depends(validation),
        user_movies_service = Depends(get_movies_service),
        ):
    await user_movies_service.patch_movie(user_movie=user_movie,token=token)

@router.get("/all",response_model=GenericResponse[UserMoviesRead])
async def get_movies(
        token: JwtInfo = Depends(validation),
        user_movies_service = Depends(get_movies_service),
        ):
    return await user_movies_service.get_movies(token=token)


@router.get("",response_model=GenericResponse[UserMovieRead])
async def get_movie(
        user_movie: UserMovieGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_movies_service = Depends(get_movies_service),
        ):
    return await user_movies_service.get_movie(user_movie=user_movie, token=token)

@router.delete("")
async def delete_movie(
        user_movie: UserMovieGet = Depends(),
        token: JwtInfo = Depends(validation),
        user_movies_service = Depends(get_movies_service),
        ):
    await user_movies_service.delete_movie(user_movie=user_movie,token=token)
