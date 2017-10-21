'''
Created on 10 ago. 2017

This will be the main GUI caller to be used as part of the GeniTools

@author: Val
'''
# -*- coding: utf-8 -*-
###########################################################################
## Python code generated with wxFormBuilder (version Aug  4 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
from gui_genitools.mainApp import AppGeni
from gui_genitools.gui_frame.main_frame import MainMenu
if __name__ == '__main__':
    app = AppGeni(False)
    frame = MainMenu(None)
    frame.get_validation_status(app.provide_validation_key())
    frame.Show(True)
    app.MainLoop()