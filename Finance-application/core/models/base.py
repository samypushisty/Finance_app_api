from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, CheckConstraint, Numeric, Boolean
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


# таблица с пользователями
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    currencies = Column(String, nullable=False)
    categories = Column(String)
    type_of_earnings = Column(String)

# таблица с едой
class CashAccount(Base):
    __tablename__ = "cash_account"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    balance = Column(Numeric, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    currency = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("type IN ('cash', 'card')", name='check_valid_type'),
    )


# таблица с сетами
class Setings(Base):
    __tablename__ = "settings"
    id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"),primary_key=True)
    theme = Column(String, nullable=False)
    language = Column(String, nullable=False)
    notifications = Column(Boolean, nullable=False)
    main_currency = Column(String, nullable=False)

    __table_args__ = (
        CheckConstraint("theme IN ('black', 'white', 'auto')", name='check_valid_type'),
        CheckConstraint("language IN ('en', 'ru')", name='check_valid_type'),
    )

class MovieOnAccount(Base):
    __tablename__ = "movie_on_account"
    id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    type = Column(String, nullable=False)
    worth = Column(Numeric, nullable=False)
    cash_account = Column(Integer, ForeignKey("cash_account.id", ondelete="CASCADE"))
    categories_name = Column(String, nullable=False)
    earnings_type = Column(String, nullable=False)
    time = Column(TIMESTAMP, default=datetime.now(timezone.utc).replace(tzinfo=None))

    __table_args__ = (
        CheckConstraint("type IN ('earning', 'outlay')", name='check_valid_type'),
    )

class Balance(Base):
    __tablename__ = "balance"
    id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    total_balance = Column(Numeric, nullable=False)
    balances_history = Column(String,nullable=False)
