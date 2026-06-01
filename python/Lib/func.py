class Data:
    def __init__(self):
        self.__request = 0

    def increment(self):
        self.__request = self.__request + 1

    def get_request(self):
        return str(self.__request)