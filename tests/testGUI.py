'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from gui_genitools.gui_frame.geni_key_frame import GeniKeyInput
from gui_genitools.mainApp import AppGeni
from gui_genitools.gui_frame.main_frame import MainMenu
import wx
import os

class Test(unittest.TestCase):


    def test_main_app(self):
        '''
        Test Main app opening
        '''
        new_env = dict(os.environ)
        new_env['DISPLAY'] = '0.0'
        app = AppGeni(False)
        frame = MainMenu(None)
        frame.get_validation_status(True)
        assert(frame.validation_status)
        frame.get_validation_status(False)
        self.assertFalse(frame.validation_status)
    def testGUIAPP(self):
        '''
        Simply test of opening the main App
        '''
        new_env = dict(os.environ)
        new_env['DISPLAY'] = '0.0'
        app = wx.App(False)
        geniKey = GeniKeyInput(None)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGUIAPP']
    unittest.main()