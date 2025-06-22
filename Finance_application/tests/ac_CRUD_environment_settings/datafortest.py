from core.redis_db.redis_helper import redis_client
from decimal import Decimal, ROUND_HALF_UP


class DataForTestUserCategories:
    def __init__(self):
        self.input = {
            "month_limit": 1,
            "name": "string",
            "currency": "USD"
        }


        self.wrong_limit = {
            "month_limit": -1,
            "name": "string",
            "currency": "USD"
        }

        self.new_wrong_limit = {
            "table_id": 2,
            "month_limit": -1,
            "name": "string",
            "currency": "USD"
        }

        self.new_wrong_id = {
            "table_id": 8,
            "month_limit": 1,
            "name": "string",
            "currency": "USD"
        }
        self.new_id_2 = {
            "table_id": 2,
            "month_limit": 100,
            "name": "string",
            "description": "something",
            "currency": "BYN"
        }

        self.new_id_4 = {
            "table_id": 4,
            "month_limit": 100,
            "name": "string",
            "description": "something",
            "currency": "BYN"
        }
        self.for_test = {
            "table_id": 1,
            # убрать в конце
            "chat_id": 9999999999,
            "month_limit": 1,
            "name": "string",
            "description": None,
            "currency": "USD",
            "balance": "0.00"
        }

        self.for_test_patch = {
            "table_id": 1,
            # убрать в конце
            "chat_id": 9999999999,
            "month_limit": 100,
            "name": "string",
            "description": "something",
            "currency": "BYN",
            "balance": "0.00"
        }

class DataForTestCashAccounts:
    def __init__(self):
        self.input = {
            "name": "string",
            "type": "cash",
            "currency": "USD"
        }
        
        self.wrong_description = {
            "name": "string",
            "description": "string"*50,
            "type": "cash",
            "currency": "USD"
        }

        self.new_wrong_id = {
            "table_id": -2,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "BYN"
        }
        self.new_id_2 = {
            "table_id": 2,
            "name": "stringn",
            "description": "stringn",
            "currency": "BYN"
        }

        self.new_id_4 = {
            "table_id": 4,
            "name": "stringn",
            "description": "stringn",
            "currency": "BYN"
        }
        self.for_test = {
            "table_id": 1,
            "balance": "0.00",
            # убрать в конце
            "chat_id": 9999999999,
            "name": "string",
            "description": None,
            "type": "cash",
            "currency": "USD"
        }

        self.for_test_patch = {
            "table_id": 1,
            "balance": "0.00",
            # убрать в конце
            "chat_id": 9999999999,
            "name": "stringn",
            "description": "stringn",
            "type": "cash",
            "currency": "BYN"
        }


class DataForTestCurrencies:
    def __init__(self):
        self.input = {
            "name": "JPY",
        }

        self.wrong_currency = {
            "name": "string",
        }


class DataForTestTypeEarnings:
    def __init__(self):
        self.input = {
            "name": "string",
            "currency": "USD"
        }


        self.wrong_name = {
            "name": "stringeringqwertyui",
            "description": "string",
            "currency": "USD"
        }


        self.new_wrong_name = {
            "table_id": 2,
            "name": "stringeringqwertyui",
            "description": "string",
            "currency": "USD"
        }

        self.new_wrong_id = {
            "table_id": -2,
            "name": "stringe",
            "description": "string"
        }
        self.new_id_2 = {
            "table_id": 2,
            "name": "strin",
            "description": "string1",
            "currency": "BYN"
        }

        self.new_id_4 = {
            "table_id": 4,
            "name": "strin",
            "description": "string1",
            "currency": "BYN"
        }
        self.for_test = {
            "table_id": 1,
            # убрать в конце
            "chat_id": 9999999999,
            "name": "string",
            "description": None,
            "currency": "USD",
            "balance": "0.00"
        }

        self.for_test_patch = {
            "table_id": 1,
            # убрать в конце
            "chat_id": 9999999999,
            "name": "strin",
            "description": "string1",
            "currency": "BYN",
            "balance": "0.00"
        }
