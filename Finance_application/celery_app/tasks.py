from decimal import Decimal, ROUND_HALF_UP
from typing import Sequence

import requests
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from celery_app.app import celery_app
from celery_app.config import  settings
from core.models.base import CashAccount, Balance, UserSettings
from core.models.db_helper import sync_db_helper

from core.redis_db.redis_helper import redis_local_client

@celery_app.task(
    name='update_prices',
)
def update_prices():
    try:
        response = requests.get(f"https://v6.exchangerate-api.com/v6/{settings.API_key}/latest/USD")
        response = response.json()["conversion_rates"]
        for k,v in response.items():
            redis_local_client.set(k, v)
        return "Success"
    except Exception as e:
        return e

@celery_app.task(
    name='balances_history',
)
def balances_history():
    try:
        with sync_db_helper.session_getter() as session:
            with session.begin():
                query = (
                    select(Balance)
                )
                balances: Result = session.execute(query)
                balances: Sequence[Balance] = list(balances.scalars().all())
                for balance in balances:
                    chat_id = balance.chat_id
                    query = (select(CashAccount).
                             options(selectinload(CashAccount.currencies_earnings),
                                     selectinload(CashAccount.currencies_outlays)).
                             filter_by(chat_id=chat_id)
                             )
                    cash_accounts: Result = session.execute(query)
                    cash_accounts: Sequence[CashAccount] = cash_accounts.scalars().all()

                    if not cash_accounts:
                        balance.balances_history.append(Decimal("0.00"))
                        continue

                    query = (select(UserSettings).
                             filter_by(chat_id=chat_id)
                             )
                    user_settings: Result = session.execute(query)
                    user_settings: UserSettings = user_settings.scalars().first()
                    target_currency = user_settings.main_currency
                    price_base = Decimal(redis_local_client.get(target_currency))

                    amount_currencies = {}
                    for cash_account in cash_accounts:
                        for currencies_earnings in cash_account.currencies_earnings:
                            if not currencies_earnings.currency in amount_currencies:
                                amount_currencies[currencies_earnings.currency] = currencies_earnings.amount
                            else:
                                amount_currencies[currencies_earnings.currency] += currencies_earnings.amount
                    for cash_account in cash_accounts:
                        for currencies_outlays in cash_account.currencies_outlays:
                            amount_currencies[currencies_outlays.currency] -= currencies_outlays.amount

                    cash_account_balance = Decimal('0.00').quantize(Decimal('0.00'))
                    for currency, amount in amount_currencies.items():
                        if target_currency == currency:
                            cash_account_balance += amount
                            continue
                        price_convert = Decimal(redis_local_client.get(currency))
                        converted_amount = (amount / price_convert * price_base).quantize(
                            Decimal("0.00"),
                            rounding=ROUND_HALF_UP)
                        cash_account_balance += converted_amount
                    balance.balances_history.append(cash_account_balance)
        return "Success "
    except Exception as e:
        return e
