import unittest
import aerochat.database

class TestJson(unittest.TestCase):
    @staticmethod
    def get_json_string():
        return '{"timestamp":"1399589150","sender":"mpillar","text":"This is a test"}'

    @staticmethod
    def get_json_message():
        return aerochat.database.Message.from_json(TestJson.get_json_string())

    def verify_json_message(self, message):
        self.assertEqual(message.timestamp, int(1399589150))
        self.assertEqual(message.sender, 'mpillar')
        self.assertEqual(message.text, 'This is a test')

    def test_json_decode(self):
        """
        Decode a JSON message and verify that we get back what we expect.
        """
        message = TestJson.get_json_message()
        self.verify_json_message(message)

    def test_json_encode(self):
        """
        Decode, encode, and verify to ensure that our encoder works as expected
        as well.
        """
        self.verify_json_message(aerochat.database.Message.from_json(TestJson.get_json_message().to_json()))

if __name__ == '__main__':
    unittest.main()