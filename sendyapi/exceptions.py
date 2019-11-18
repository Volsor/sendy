
class SendyException(Exception):

    def __init__(self, msg):
        self.msg = msg
        super().__init__()

    def __str__(self):
        return f'Sendy error: {self.msg}'


class SendyAlreadySubscribed(SendyException):
    pass


class SendyNotSubscribed(SendyException):
    pass


class SendyServerError(SendyException):
    pass
