'''
Created on 12 ago. 2017

@author: Val
'''
import wx
from gui_genitools.messages_gui import NO_VALIDATED_KEY
from gui_genitools.gui_frame.geni_key_frame import GeniKeyInput
from gui_genitools.gui_frame.geni_fs_import import GeniFsImport
from wx.lib.pubsub import pub

###########################################################################
## Class MyFrame3
###########################################################################

class MainMenu ( wx.Frame ):
    def __init__( self, parent ):
        self.status_validation = False
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 900,400 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        #Introducing the sizers
        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        #Let's set up the controls
        self.m_infoCtrl2 = wx.InfoBar( self )
        self.m_infoCtrl2.SetShowHideEffects( wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE )
        self.m_infoCtrl2.SetEffectDuration( 500 )
        bSizer2.Add( self.m_infoCtrl2, 0, wx.ALL|wx.EXPAND, 5 )
        #
        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Introduce Geni Token", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Get Ancestors", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"Get Cousins", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #
        self.m_button4 = wx.Button( self, wx.ID_ANY, u"Import Family Search to Geni", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button4, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
        #
        self.SetSizer( bSizer1 )
        self.Layout()
        self.Centre( wx.BOTH )
        # Connect Events
        self.m_button1.Bind( wx.EVT_BUTTON, self.OnClickIntroductionKey )
        self.m_button4.Bind( wx.EVT_BUTTON, self.OnClickOpenImportFSDialog )
        #Subsriptions
        pub.subscribe(self.__onGeniKeyUpdateValidation, 'geni.key.validate')
    def __del__( self ):
        pass
    def get_validation_status(self, status_validation):
        '''
        This function will provide the status of the validation of the Geni_KEY
        '''
        #If the validatin status is not correct we inform about it
        if not status_validation:
            self.m_infoCtrl2.ShowMessage(NO_VALIDATED_KEY, wx.ICON_INFORMATION)
        else:
            self.m_infoCtrl2.Close(force=False)
            self.m_infoCtrl2.Dismiss()
        self.validation_status = status_validation
    def OnClickIntroductionKey( self, event ):
        '''
        Launching the message window to introduce the Geni key
        '''
        message_genikey = GeniKeyInput(None)
        message_genikey.Show(True)
        event.Skip()
    def OnClickOpenImportFSDialog( self, event ):
        '''
        This is launching the creation of the dialog for importing FS excels
        '''
        interface_input = GeniFsImport(None)
        interface_input.Show(True)
        event.Skip()
    def __onGeniKeyUpdateValidation(self, validation_status):
        '''
        Listener that will try to remove the error message in the guy of missing
        geni key
        '''
        self.get_validation_status(validation_status)