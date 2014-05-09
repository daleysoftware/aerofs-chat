import unittest
import shutil
import tempfile
import aerochat.database

class TestGet(unittest.TestCase):
    def mock_milli_time(self):
        self.time_counter += 1
        return self.time_counter

    def setUp(self):
        self.time_counter = 0
        self.temp_dir = tempfile.mkdtemp()
        aerochat.database.current_milli_time = self.mock_milli_time

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_get_no_count(self):
        """
        Publish 100 messages, read back the latest according to our mocked time
        and make sure we're getting the correct message content.
        """
        mdb = aerochat.database.MessageDatabase("mpillar", self.temp_dir)
        for i in xrange(1,101): mdb.publish_message("Test message %i" % i)
        messages = mdb.get_latest_messages(90)
        for i in xrange(90+1, 100+1):
            self.assertEqual(messages[i-(90+1)].text, ("Test message %i" % i))

    def test_get_with_count(self):
        """
        Create 100 messages, read back the latest according to our mocked time
        and a fixed count of 1, and make sure we're getting the correct message.
        """
        mdb = aerochat.database.MessageDatabase("mpillar", self.temp_dir)
        for i in xrange(1,101): mdb.publish_message("Test message %i" % i)
        messages = mdb.get_latest_messages(90, 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual("Test message 100", messages[0].text)

if __name__ == '__main__':
    unittest.main()