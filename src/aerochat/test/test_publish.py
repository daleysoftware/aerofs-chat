import unittest
import os
import shutil
import tempfile
import aerochat.database

class TestJson(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_publish(self):
        mdb = aerochat.database.MessageDatabase("mpillar", self.temp_dir)
        message = mdb.publish_message("This is a test")
        db_file = os.path.join(self.temp_dir, str(message.timestamp))
        self.assertTrue(os.path.isfile(db_file))

if __name__ == '__main__':
    unittest.main()