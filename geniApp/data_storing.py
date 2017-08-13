'''
Created on 12 ago. 2017

@author: Val
'''
FILENAME = "genidata.out"

import shelve

class StoringKeys():
    '''
    This module is reading session data later on used by the GUI.
    '''


    def __init__(self, filename = FILENAME):
        '''
        Simple initiation of the object
        '''
        self.persistent = shelve.open(filename)
    def getGENIkey(self):
        '''
        This method provides back the data of GENI_KEY
        '''
        if("GENI_KEY" in self.persistent):
            return self.persistent["GENI_KEY"]
        else:
            return "EMPTY"
    def setGENIkey(self, geni_key):
        '''
        This function saves the geni key inside the filename
        '''
        self.persistent["GENI_KEY"] = geni_key
    def iskeypresent(self, key):
        '''
        Informs if the key is present
        '''
        return key in self.persistent
    def close(self):
        '''
        Closes the file finally.
        '''
        self.persistent.close()