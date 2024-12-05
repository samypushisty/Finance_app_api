from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.schemas.auth import UserAuth, UserJWT
from secure import create_jwt
from fastapi.exceptions import HTTPException

router = APIRouter(tags=["Auth"])


@router.post("")
async def get_users(
        user: UserAuth,
        session: AsyncSession = Depends(db_helper.session_getter),
        ):
    answer = UserJWT(jwt = create_jwt(user.chat_id))
    return HTTPException(status_code=500, detail=answer)

