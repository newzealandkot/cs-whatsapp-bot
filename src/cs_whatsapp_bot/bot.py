MESSAGE = "Welcome to Climate Service!"


class Bot:
    message = MESSAGE

    def __init__(self, sender):
        self.sender = sender

    def send_message(self):
        self.sender.send(self.message)
