import unittest
from parser_input import reader_input
import os

class testReaderInput(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2

    def testReadingProfileFile(self):
        '''
        Easy test that profile is properly read
        '''
        data = reader_input.reader_input(os.path.join(self.filelocation,"INPUT_PROFIL"))
        assert(str(data.profile) == "60000000xxxxxxxxx")
        assert(str(data.genikey) == "xxxccc")
    def testNoGeniKey(self):
        '''
        Test that no Geni key creates a stopping message
        '''
        data = reader_input.reader_input(os.path.join(self.filelocation , "INPUT_NO_GENIKEY"))
        self.assertFalse(data.genikey_given)
        self.assertFalse(data.continue_execution)
    def testNoGenerationsGiven(self):
        '''
        Test to not continue if no Generations are given
        '''
        data = reader_input.reader_input(os.path.join(self.filelocation , "INPUT_NO_GENERATIONS"))
        self.assertFalse(data.generations_given)
        self.assertFalse(data.continue_execution)
    def testNoProfileGiven(self):
        '''
        Test error if no profile is given
        '''
        data = reader_input.reader_input(os.path.join(self.filelocation , "INPUT_NO_PROFILE"))
        self.assertFalse(data.profile_given)
        self.assertFalse(data.continue_execution)
        assert( type(data.generations) is int)
        
        

