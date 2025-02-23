from datetime import datetime
from decimal import Decimal
from typing import Optional, Annotated
from sqlalchemy import ForeignKey, text, String, MetaData, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from core.config import settings
import enum

str_3 = Annotated[str,3]
str_15 = Annotated[str,15]
str_256 = Annotated[str,256]
intfk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.chat_id", ondelete="CASCADE"))]
intfkpk = Annotated[int, mapped_column(BigInteger, ForeignKey("user.chat_id", ondelete="CASCADE"), primary_key=True)]
intpk = Annotated[int, mapped_column( primary_key=True, autoincrement=True)]


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

    chat_id: Mapped[int] = mapped_column( BigInteger, primary_key=True, autoincrement=False)
    registration: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    last_visit: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class CashAccount(Base):
    __tablename__ = "cash_account"

    table_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    name: Mapped[str_15]
    description: Mapped[str_256]
    type: Mapped[CashAccountType]
    currency: Mapped[str_3]


class Category(Base):
    __tablename__ = "category"

    table_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    month_limit: Mapped[float]
    name: Mapped[str_15]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    currency: Mapped[str_3]

class Earnings(Base):
    __tablename__ = "earnings"

    table_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    name: Mapped[str_15]
    description: Mapped[str_256]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    currency: Mapped[str_3]


# таблица с сетами
class UserSettings(Base):
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

    table_id: Mapped[intpk]
    chat_id: Mapped[intfk]
    title: Mapped[str_15]
    description: Mapped[Optional[str_256]]
    type: Mapped[MovieType]
    worth: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    currency: Mapped[str_3]
    base_worth: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    cash_account: Mapped[int] = mapped_column(ForeignKey("cash_account.table_id", ondelete="CASCADE"))
    categories_id: Mapped[Optional[int]] = mapped_column(None, ForeignKey("category.table_id", ondelete="CASCADE"))
    earnings_id: Mapped[Optional[int]] = mapped_column(None, ForeignKey("earnings.table_id", ondelete="CASCADE"))
    time: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class Balance(Base):
    __tablename__ = "balance"
    chat_id: Mapped[intfkpk]
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=100, scale=2))
    balances_history: Mapped[str]
