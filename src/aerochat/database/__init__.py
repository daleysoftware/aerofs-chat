import json
import os
import time
import threading

current_milli_time = lambda: int(round(time.time() * 1000))

class Message:
    def __init__(self, timestamp, sender, text):
        self.timestamp = int(timestamp)
        self.sender = sender.encode('utf-8')
        self.text = text.encode('utf-8')

    @staticmethod
    def from_json(json_string):
        """
        Convert a message to JSON format.
        """
        parsed = json.loads(json_string)
        return Message(parsed['timestamp'], parsed['sender'], parsed['text'])

    def to_json(self):
        """
        Parse a message from JSON format.
        """
        return '{"timestamp":"%s","sender":"%s","text":"%s"}' % (str(self.timestamp), self.sender, self.text)

class MessageDatabase:
    def __init__(self, sender, db_dir):
        self.sender = sender
        self.db_dir = db_dir
        if not os.path.isdir(self.db_dir):
            raise IOError("%s does not exist", self.db_dir)

    def publish_message(self, text):
        """
        Publish a message with the given `text` to the AeroChat databse. Other
        users in the chatroom will receive this message.
        """
        timestamp = current_milli_time()
        message = Message(timestamp, self.sender, text)
        db_file = os.path.join(self.db_dir, str(timestamp))
        with open(db_file, "w+") as f: f.write(message.to_json())
        return message

    @staticmethod
    def _sorted_ls(path):
        ctime = lambda f: int(f)
        return list(sorted(os.listdir(path), key=ctime))

    def get_latest_messages(self, after_date=0, count=0):
        """
        Get the latest messages in the AeroChat database after the given date
        `after_date` which is formatted in epoch time. Limit the number of items
        in our reply to `count`. Always return the newest items where possible.
        """
        sorted_files = MessageDatabase._sorted_ls(self.db_dir)
        files_to_parse = []
        for f in sorted_files:
            if int(f) > after_date:
                files_to_parse.append(f)
        result = []
        for f in files_to_parse[-count:]:
            with open(os.path.join(self.db_dir, f), "r") as fd:
                result.append(Message.from_json(fd.read()))
        return result

class MessagePoller(threading.Thread):
    def __init__(self, mdb, last_timestamp, callback):
        threading.Thread.__init__(self)
        self.mdb = mdb
        self.last_timestamp = last_timestamp
        self.callback = callback
        self.more_todo = True

    def stop(self):
        self.more_todo = False

    def run(self):
        while self.more_todo:
            # Poll for messages
            messages = self.mdb.get_latest_messages(self.last_timestamp)

            if len(messages) > 0:
                self.last_timestamp = messages[-1].timestamp
                self.callback(messages)

            # Sleep for a small amount of time.
            time.sleep(0.3)
