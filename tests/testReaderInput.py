import unittest
from parser_input import reader_input
import os

class testReaderInput(unittest.TestCase):
    def setUp(self):
        self.filelocation = os.path.join(os.getcwd(), "fixtures_files", "INPUT_PROFIL")

    def testReadingProfileFile(self):
        '''
        Easy test that profile is properly read
        '''
        data = reader_input.reader_input(self.filelocation)
        assert(str(data.profile) == "60000000xxxxxxxxx")

