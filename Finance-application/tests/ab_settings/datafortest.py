class DataForTestSettings:
    def __init__(self):
        self.new_data_param = {
            "theme": "white",
            "language": "russian",
            "notifications": False,
            "main_currency": "byn"
        }

        self.new_wrong_data_param = {
            "theme": "white",
            "language": "rus",
            "notifications": False,
            "main_currency": "byn"
        }

        self.old_data_param = {
            "theme": "auto",
            "language": "english",
            "notifications": True,
            "main_currency": "usd"
        }