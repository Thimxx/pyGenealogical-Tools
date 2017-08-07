import unittest
import os

if __name__ == '__main__':
    print(os.environ.get('GENI_KEY'))

    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=2).run(testsuite)