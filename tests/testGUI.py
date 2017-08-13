'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from gui_genitools.gui_frame.geni_key_frame import GeniKeyInput
import wx
import os

class Test(unittest.TestCase):


    def testGUIAPP(self):
        '''
        Simply test of opening the main App
        '''
        new_env = dict(os.environ)
        new_env['DISPLAY'] = '0.0'
        #app = wx.App(False)
        #geniKey = GeniKeyInput(None)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGUIAPP']
    unittest.main()