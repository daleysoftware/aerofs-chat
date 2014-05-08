import json
import os
import time

current_milli_time = lambda: int(round(time.time() * 1000))

class Message:
    def __init__(self, timestamp, sender, text):
        self.timestamp = int(timestamp)
        self.sender = sender.encode('utf-8')
        self.text = text.encode('utf-8')

    @staticmethod
    def from_json(json_string):
        parsed = json.loads(json_string)
        return Message(parsed['timestamp'], parsed['sender'], parsed['text'])

    def to_json(self):
        return '{"timestamp":"%s","sender":"%s","text":"%s"}' % (str(self.timestamp), self.sender, self.text)

class MessageDatabase:
    def __init__(self, sender, db_dir):
        self.sender = sender
        self.db_dir = db_dir

        if not os.path.isdir(self.db_dir):
            raise IOError("%s does not exist", self.db_dir)

    def publish_message(self, text):
        timestamp = current_milli_time()
        message = Message(timestamp, self.sender, text)

        db_file = os.path.join(self.db_dir, str(timestamp))
        with open(db_file, "w+") as f:
            f.write(message.to_json())

        return message

    def get_latest_messages(self, after_date=0):
        # TODO
        pass
