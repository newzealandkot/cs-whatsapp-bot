class FakeMessageSender:

    def __init__(self):
        self.total_messages = 0

    def send(self, message):
        self.total_messages += 1
