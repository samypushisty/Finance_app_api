from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.models.base import User, Settings
from core.schemas.auth import UserAuth, UserRegistration
from core.schemas.user_settings import UserSettingsRead
from secure import create_jwt
from fastapi.exceptions import HTTPException
from sqlalchemy import select


router = APIRouter(tags=["Auth"])


@router.post("")
async def get_users(
        user: UserAuth,
        session: AsyncSession = Depends(db_helper.session_getter),
        ):
    query = select(User).where(User.chat_id == user.chat_id)
    result = await session.execute(query)
    result = result.scalars().all()
    if not result:
        user_registration = UserRegistration(chat_id=user.chat_id,currencies="_",type_of_earnings="_" )
        user_settings = UserSettingsRead(chat_id=user.chat_id,theme="auto",language="english",notifications=True,main_currency="usd")
        stmt = User(**user_registration.model_dump())
        session.add(stmt)
        await session.flush()
        stmt = Settings(**user_settings.model_dump())
        session.add(stmt)
        await session.commit()
    answer = create_jwt(user.chat_id)
    return HTTPException(status_code=500, detail=answer)

