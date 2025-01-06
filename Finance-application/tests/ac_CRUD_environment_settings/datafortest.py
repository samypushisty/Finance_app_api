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
            "currency": "str"
        }


        self.wrong_balance = {
            "balance": -10,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "str"
        }
        
        self.wrong_description = {
            "balance": 10,
            "name": "string",
            "description": "string"*50,
            "type": "cash",
            "currency": "str"
        }

        self.new_wrong_balance = {
            "cash_id": 2,
            "balance": -10,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "str"
        }

        self.new_wrong_id = {
            "cash_id": -2,
            "balance": 10,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "str"
        }
        self.new_id_2 = {
            "cash_id": 2,
            "balance": 100,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
            "currency": "byn"
        }

        self.new_id_4 = {
            "cash_id": 4,
            "balance": 100,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
            "currency": "byn"
        }
        self.for_test = {
            "cash_id": 1,
            "chat_id": 9999999999,
            "balance": 10.0,
            "name": "string",
            "description": "string",
            "type": "cash",
            "currency": "str"
        }

        self.for_test_patch = {
            "cash_id": 1,
            "chat_id": 9999999999,
            "balance": 100.0,
            "name": "stringn",
            "description": "stringn",
            "type": "card",
            "currency": "byn"
        }
