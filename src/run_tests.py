import unittest
import aerochat.test
test_suite = aerochat.test.create_test_suite()
text_runner = unittest.TextTestRunner().run(test_suite)
