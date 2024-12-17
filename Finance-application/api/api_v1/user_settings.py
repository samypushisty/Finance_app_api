from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from core.schemas.user_settings import UserSettingsPatch, UserSettingsRead
from core.models.base import Settings
from secure import JwtInfo
from sqlalchemy import select

from secure.jwt_functions import validation

router = APIRouter(tags=["Settings"])


@router.patch("")
async def get_users(
        user_settings: UserSettingsPatch,
        token: JwtInfo = Depends(validation),
        session: AsyncSession = Depends(db_helper.session_getter),
        ):
    query = select(Settings).filter(Settings.chat_id == token.id)
    user_settings_old = await session.execute(query)
    user_settings_old = user_settings_old.scalars().first()
    for key in user_settings.model_dump().keys():
        if getattr(user_settings, key):
            setattr(user_settings_old, key, getattr(user_settings, key))
    await session.commit()

@router.get("",response_model=UserSettingsRead)
async def get_users(
        jwt: str,
        session: AsyncSession = Depends(db_helper.session_getter),
        ):
    token = JwtInfo(jwt)
    query = select(Settings).where(Settings.chat_id == token.id)
    result = await session.execute(query)
    result = result.scalars().first()
    return result