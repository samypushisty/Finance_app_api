class DataForTestUserEnvironment:
    def __init__(self):
        self.data_param = {
            "month_limit": 1,
            "name": "string"
        }

        self.data_param_for_test = {
            "category_id": 1,
            "chat_id": 9999999999,
            "month_limit": 1,
            "name": "string"
        }

        self.wrong_data_param = {
            "month_limit": -1,
            "name": "string"
        }

        self.new_data_param_2 = {
            "category_id": 2,
            "month_limit": 100,
            "name": "string"
        }

        self.new_wrong_data_param = {
            "category_id": 2,
            "month_limit": -1,
            "name": "string"
        }

        self.new_data_param_4 = {
            "category_id": 4,
            "month_limit": 100,
            "name": "string"
        }

        self.data_param_for_test_patch = {
            "category_id": 1,
            "chat_id": 9999999999,
            "month_limit": 100,
            "name": "string"
        }

