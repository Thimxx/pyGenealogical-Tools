'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from gui_genitools.gui_frame.geni_key_frame import GeniKeyInput
import wx

class Test(unittest.TestCase):


    def testGUIAPP(self):
        '''
        Simply test of opening the main App
        '''
        app = wx.App(False)
        geniKey = GeniKeyInput(None)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGUIAPP']
    unittest.main()