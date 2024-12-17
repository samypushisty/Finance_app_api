from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from sqlalchemy import ForeignKey, text, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from core.config import settings
import enum

str_3 = Annotated[str,3]
str_15 = Annotated[str,15]
str_256 = Annotated[str,256]
intfk = Annotated[int, mapped_column(ForeignKey("user.chat_id", ondelete="CASCADE"))]
intfkpk = Annotated[int, mapped_column(ForeignKey("user.chat_id", ondelete="CASCADE"), primary_key=True)]
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )
    type_annotation_map = {
        str_3: String(3),
        str_15: String(15),
        str_256: String(256)
    }


class Language(enum.Enum):
    english = "english"
    russian = "russian"

class CashAccountType(enum.Enum):
    cash = "cash"
    card = "card"

class MovieType(enum.Enum):
    earning = "earning"
    outlay = "outlay"

class Theme(enum.Enum):
    black = "black"
    white = "white"
    auto = "auto"


class User(Base):
    __tablename__ = "user"

    chat_id: Mapped[intpk]
    currencies: Mapped[str]
    type_of_earnings: Mapped[Optional[str]]


class CashAccount(Base):
    __tablename__ = "cash_account"

    cash_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    balance: Mapped[float]
    name: Mapped[str_15]
    description: Mapped[str_256]
    type: Mapped[CashAccountType]
    currency: Mapped[str_3]


class Category(Base):
    __tablename__ = "category"
    chat_id: Mapped[intfkpk]
    month_limit: Mapped[float]
    name: Mapped[str_15]


# таблица с сетами
class Settings(Base):
    __tablename__ = "settings"

    chat_id: Mapped[intfkpk]
    theme: Mapped[Theme]
    language: Mapped[Language]
    notifications: Mapped[bool]
    main_currency: Mapped[str_3]

    class Config:
        use_enum_values = True

class MovieOnAccount(Base):
    __tablename__ = "movie_on_account"

    movie_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    title: Mapped[str_15]
    description: Mapped[Optional[str_256]]
    type: Mapped[MovieType]
    worth: Mapped[Decimal]
    cash_account: Mapped[int] = mapped_column(ForeignKey("cash_account.cash_id", ondelete="CASCADE"))
    categories_name: Mapped[Optional[str]]
    earnings_type: Mapped[Optional[str]]
    time: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Balance(Base):
    __tablename__ = "balance"
    chat_id: Mapped[intfkpk]
    total_balance: Mapped[float]
    balances_history: Mapped[str]
