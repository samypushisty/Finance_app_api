class DataForTestUserEnvironment:
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

