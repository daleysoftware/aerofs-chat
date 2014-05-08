import glob
import unittest

def create_test_suite():
    test_file_strings = glob.glob('aerochat/test/test_*.py')
    module_strings = ['aerochat.test.'+s.split('/')[-1].split('.')[0] for s in test_file_strings]
    suites = [unittest.defaultTestLoader.loadTestsFromName(name) \
              for name in module_strings]
    test_suite = unittest.TestSuite(suites)
    return test_suite
