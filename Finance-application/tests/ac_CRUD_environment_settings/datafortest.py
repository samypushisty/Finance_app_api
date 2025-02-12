class DataForTestUserCategories:
    def __init__(self):
        self.input = {
            "month_limit": 1,
            "name": "string"
        }


        self.wrong_limit = {
            "month_limit": -1,
            "name": "string"
        }

        self.new_wrong_limit = {
            "category_id": 2,
            "month_limit": -1,
            "name": "string"
        }

        self.new_wrong_id = {
            "category_id": 8,
            "month_limit": 1,
            "name": "string"
        }
        self.new_id_2 = {
            "category_id": 2,
            "month_limit": 100,
            "name": "string"
        }

        self.new_id_4 = {
            "category_id": 4,
            "month_limit": 100,
            "name": "string"
        }
        self.for_test = {
            "category_id": 1,
            "chat_id": 9999999999,
            "month_limit": 1,
            "name": "string"
        }

        self.for_test_patch = {
            "category_id": 1,
            "chat_id": 9999999999,
            "month_limit": 100,
            "name": "string"
        }

class DataForTestCashAccounts:
    def __init__(self):
        self.input = {
            "balance": 10,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "USD"
        }


        self.wrong_balance = {
            "balance": -10,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "USD"
        }
        
        self.wrong_description = {
            "balance": 10,
            "name": "string",
            "description": "string"*50,
            "type": "cash",
            "currency": "USD"
        }

        self.new_wrong_id = {
            "cash_id": -2,
            "name": "string",
            "description": "string",
            "type": "cash",
        }
        self.new_id_2 = {
            "cash_id": 2,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
        }

        self.new_id_4 = {
            "cash_id": 4,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
        }
        self.for_test = {
            "cash_id": 1,
            "balance": 10,
            "chat_id": 9999999999,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "USD"
        }

        self.for_test_patch = {
            "cash_id": 1,
            "balance": 10,
            "chat_id": 9999999999,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
            "currency": "USD"
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
            "description": "string"
        }


        self.wrong_name = {
            "name": "stringeringqwertyui",
            "description": "string"
        }


        self.new_wrong_name = {
            "earning_id": 2,
            "name": "stringeringqwertyui",
            "description": "string"
        }

        self.new_wrong_id = {
            "earning_id": -2,
            "name": "stringe",
            "description": "string"
        }
        self.new_id_2 = {
            "earning_id": 2,
            "name": "strin",
            "description": "string1"
        }

        self.new_id_4 = {
            "earning_id": 4,
            "name": "strin",
            "description": "string1"
        }
        self.for_test = {
            "earning_id": 1,
            "chat_id": 9999999999,
            "name": "string",
            "description": "string"
        }

        self.for_test_patch = {
            "earning_id": 1,
            "chat_id": 9999999999,
            "name": "strin",
            "description": "string1"
        }
