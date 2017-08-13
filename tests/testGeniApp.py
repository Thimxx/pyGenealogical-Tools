'''
Created on 12 ago. 2017

@author: Val
'''
import unittest, os, time
from geniApp.data_storing import StoringKeys
from random import randrange
from tests.FIXTURES import GENI_KEY_EXAMPLE

class Test(unittest.TestCase):
    '''
    This function tests the global geniApp functionality.
    '''

    def testGENIkeyNotExisting(self):
        '''
        Testing data is providing although GENI key not existing.
        '''
        irand = randrange(0, 1000000)
        filename = "testData" + str(irand) + "--" + time.strftime("%d.%m.%Y")
        d = StoringKeys(filename)
        assert(not d.iskeypresent("GENI_KEY"))
        assert(d.getGENIkey() == "EMPTY")
        d.close()
        
        delete_files(filename)
    
    def testReadingGENIkey(self):
        '''
        Testing creating and reading back GENIkey
        '''
        irand = randrange(1000000, 2000000)
        filename2 = "testData" + str(irand) + "--" + time.strftime("%d.%m.%Y")
        d = StoringKeys(filename2)
        assert(not d.iskeypresent("GENI_KEY"))
        d.setGENIkey(GENI_KEY_EXAMPLE)
        d.close()
        del d
        
        d2 = StoringKeys(filename2)
        assert(d2.iskeypresent("GENI_KEY"))
        assert(d2.getGENIkey() == GENI_KEY_EXAMPLE)
        
        delete_files(filename2)

def  delete_files(file_name):
    '''
    Common function to delete generated temporary files
    '''
    my_dir = "./"
    for fname in os.listdir(my_dir):
        if fname.startswith(file_name):
            os.remove(os.path.join(my_dir, fname))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()