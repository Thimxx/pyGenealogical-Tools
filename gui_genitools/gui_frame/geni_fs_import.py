'''
Created on 29 oct. 2017

@author: Val
'''

###########################################################################
## Python code generated with wxFormBuilder (version Aug  4 2017)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame31
###########################################################################

class GeniFsImport ( wx.Frame ):
    '''
    Class the handles the import interface for the FamilySearch output file
    '''
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        #Introducing the sizer
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        #Introducing the buttons
        self.m_button6 = wx.Button( self, wx.ID_ANY, u"Introduce FS export", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer4.Add( self.m_button6, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #Assigning sizer and layout plus parameters
        self.SetSizer( bSizer4 )
        self.Layout()
        self.Centre( wx.BOTH )
    def __del__( self ):
        pass