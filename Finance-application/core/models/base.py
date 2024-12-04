from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from sqlalchemy import ForeignKey, text, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from core.config import settings
import enum

str_5 = Annotated[str,5]
str_50 = Annotated[str,50]
str_256 = Annotated[str,256]
intfk = Annotated[int, mapped_column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)]
intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention
    )
    type_annotation_map = {
        str_5: String(5),
        str_50: String(50),
        str_256: String(256)
    }


class Language(enum.Enum):
    english = "en"
    russian = "ru"

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

# таблица с пользователями
class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    currencies: Mapped[str]
    categories: Mapped[Optional[str]]
    type_of_earnings: Mapped[Optional[str]]


# таблица с едой
class CashAccount(Base):
    __tablename__ = "cash_account"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    balance: Mapped[float]
    name: Mapped[str_50]
    type: Mapped[CashAccountType]
    currency: Mapped[str_5]


# таблица с сетами
class Setings(Base):
    __tablename__ = "settings"

    id: Mapped[intfk]
    theme: Mapped[Theme]
    language: Mapped[Language]
    notifications: Mapped[bool]
    main_currency: Mapped[str_5]


class MovieOnAccount(Base):
    __tablename__ = "movie_on_account"

    id: Mapped[intfk]
    title: Mapped[str_50]
    description: Mapped[Optional[str_256]]
    type: Mapped[MovieType]
    worth: Mapped[Decimal]
    cash_account: Mapped[int] = mapped_column(ForeignKey("cash_account.id", ondelete="CASCADE"))
    categories_name: Mapped[str]
    earnings_type: Mapped[str]
    time: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Balance(Base):
    __tablename__ = "balance"
    id: Mapped[intfk]
    total_balance: Mapped[float]
    balances_history: Mapped[str]
