import unittest
from parser_input import reader_input
import os

class testReaderInput(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        location1 = os.path.join(os.getcwd(), "fixtures_files", "INPUT_PROFIL")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files", "INPUT_PROFIL")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2

    def testReadingProfileFile(self):
        '''
        Easy test that profile is properly read
        '''
        data = reader_input.reader_input(self.filelocation)
        assert(str(data.profile) == "60000000xxxxxxxxx")
        assert(str(data.genikey) == "xxxccc")

