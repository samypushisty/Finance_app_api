from unicodedata import category


class DataForTestMovieOnAccount:
    def __init__(self):
        self.input_e2_c2 = {
            "title": "string",
            "type": "earning",
            "worth": 1000,
            "currency": "USD",
            "cash_account": 2,
            "earnings_id": 2

        }
        self.input_e3_c3 = {
            "title": "string",
            "description": "string",
            "type": "earning",
            "worth": 1000,
            "currency": "USD",
            "cash_account": 3,
            "earnings_id": 3
        }

        self.input_o2_c2 = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "USD",
            "cash_account": 2,
            "categories_id": 2
        }
        self.input_o3_c3 = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "USD",
            "cash_account": 3,
            "categories_id": 3
        }
        self.input_wrong_user_e = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 2000,
            "currency": "USD",
            "cash_account": 3,
            "categories_id": 3
        }
        self.input_wrong_user_o = {
            "title": "string",
            "description": "string",
            "type": "earning",
            "worth": 2000,
            "currency": "USD",
            "cash_account": 3,
            "earnings_id": 3
        }
        self.input_wrong_balance_0 = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 2000,
            "currency": "USD",
            "cash_account": 3,
            "categories_id": 3
        }


        self.wrong_currency = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "categories_id": 3
        }
        
        self.wrong_cash_id = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 1,
            "categories_id": 3
        }
        self.wrong_category_id = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "categories_id": 1
        }
        self.wrong_type_o = {
            "title": "string",
            "description": "string",
            "type": "earning",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "categories_id": 2
        }
        self.wrong_type_e = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "earnings_id": 2
        }
        self.wrong_not_type = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "earnings_id": 2
        }
        self.wrong_all_type = {
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": 100,
            "currency": "rus",
            "cash_account": 3,
            "earnings_id": 2
        }


        self.new_wrong_id = {
            "table_id": 0,
            "title": "string",
            "description": "string",
            "worth": 1,
            "currency": "usd"
        }

        self.new_wrong_currency = {
            "table_id": 1,
            "title": "string",
            "description": "string",
            "worth": 1,
            "currency": "str"
        }

        self.new_wrong_balance_0 = {
            "table_id": 1,
            "title": "string",
            "description": "string",
            "worth": 1,
            "currency": "usd"
        }

        self.new_id_1 = {
            "table_id": 1,
            "worth": 1200,
            "description": "string"
        }

        self.new_id_2 = {
            "table_id": 2,
            "currency": "EUR"
        }
        self.new_id_3 = {
            "table_id": 3,
            "worth": 400
        }
        self.new_id_4 = {
            "table_id": 4,
            "currency": "eur"
        }

        self.for_test = [
            {
            "chat_id": 9999999999,
            "table_id": 1,
            "title": "string",
            "description": None,
            "type": "earning",
            "worth": "1000.00",
            "currency": "USD",
            "cash_account": 2,
            "earnings_id": 2,
            "categories_id": None
        },
        {
            "chat_id": 9999999999,
            "table_id": 2,
            "title": "string",
            "description": "string",
            "type": "earning",
            "worth": "1000.00",
            "currency": "USD",
            "cash_account": 3,
            "earnings_id": 3,
            "categories_id": None
        },
        {
            "chat_id": 9999999999,
            "table_id": 3,
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": "100.00",
            "currency": "USD",
            "cash_account": 2,
            "categories_id": 2,
            "earnings_id": None
        },
        {
            "chat_id": 9999999999,
            "table_id": 4,
            "title": "string",
            "description": "string",
            "type": "outlay",
            "worth": "100.00",
            "currency": "USD",
            "cash_account": 3,
            "categories_id": 3,
            "earnings_id": None
        }]

        self.for_test_patch = [
            {
                "chat_id": 9999999999,
                "table_id": 1,
                "title": "string",
                "description": "string",
                "type": "earning",
                "worth": "1200.00",
                "currency": "USD",
                "cash_account": 2,
                "earnings_id": 2,
                "categories_id": None
            },
            {
                "chat_id": 9999999999,
                "table_id": 2,
                "title": "string",
                "description": "string",
                "type": "earning",
                "worth": "1000.00",
                "currency": "EUR",
                "cash_account": 3,
                "earnings_id": 3,
                "categories_id": None
            },
            {
                "chat_id": 9999999999,
                "table_id": 3,
                "title": "string",
                "description": "string",
                "type": "outlay",
                "worth": "400.00",
                "currency": "USD",
                "cash_account": 2,
                "categories_id": 2,
                "earnings_id": None
            }
            ]
