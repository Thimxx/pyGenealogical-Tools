'''
Created on 13 ago. 2017

@author: Val
'''
import unittest
from gui_genitools.gui_frame.geni_key_frame import GeniKeyInput
from gui_genitools.mainApp import AppGeni
from gui_genitools.gui_frame.main_frame import MainMenu
from gui_genitools.gui_frame.geni_fs_import import GeniFsImport
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
        
        self.assertFalse(app.provide_validation_key())
        
        #This one checks to call the geni_fs_import
        evt2 = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,frame.m_button4.GetId())
        frame.OnClickIntroductionKey(evt2)
        #Let's call the geni key caller
        evt = wx.PyCommandEvent(wx.EVT_BUTTON.typeId,frame.m_button1.GetId())
        frame.OnClickIntroductionKey(evt)
    def testGUIAPP(self):
        '''
        Simply test of opening the main App
        '''
        new_env = dict(os.environ)
        new_env['DISPLAY'] = '0.0'
        app = wx.App(False)
        geniKey = GeniKeyInput(None)
    
    def test_fs_import(self):
        '''
        Test fs import function
        '''
        new_env = dict(os.environ)
        new_env['DISPLAY'] = '0.0'
        app = wx.App(False)
        geniKey = GeniFsImport(None)
        
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testGUIAPP']
    unittest.main()