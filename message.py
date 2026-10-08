
class Message:
    def __init__(self, sender, text, day_sent, time_sent):
        self.sender = sender
        self.text = text
        self.day_sent = day_sent
        self.time_sent = time_sent

    def to_dict(self):
        return {
            "sender": self.sender,

            "text": self.text,

            "day_sent": self.day_sent,

            "time_sent": self.time_sent
        }
    
    def load_from_dict(self, data):
        self.sender = data["sender"]
        self.text = data["text"]
        self.day_sent = data["day_sent"]
        self.time_sent = data["time_sent"]