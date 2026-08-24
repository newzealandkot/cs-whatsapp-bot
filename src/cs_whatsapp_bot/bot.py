MESSAGE = "Welcome to Climate Service!"


class BotInactiveError(Exception):
    """Raised when bot is inactive"""


class Bot:

    def __init__(self):
        self.is_active = False

    def start(self):
        self.is_active = True

    def stop(self):
        self.is_active = False

    def message(self):
        if self.is_active:
            return MESSAGE
        raise BotInactiveError()
