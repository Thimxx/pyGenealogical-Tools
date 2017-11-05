'''
Created on 13 ago. 2017

@author: Val
'''
import wx
import wx.xrc, wx.adv
from gui_genitools.messages_gui import MESSAGE_GENI_KEY_ADDRESS
from wx.lib.pubsub import pub

###########################################################################
## Class GeniKeyInput
###########################################################################

class GeniKeyInput ( wx.Frame ):
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 700,202 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        #Including the sizers for centering the buttons
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)
        #We sett the info of each button
        self.Text_geni_key = wx.StaticText( self, wx.ID_ANY, MESSAGE_GENI_KEY_ADDRESS, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.Text_geni_key.Wrap( -1 )
        bSizer4.Add( self.Text_geni_key, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        #Adding the link to the error message related to the lack of token
        self.link = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, label="this page", url="https://www.geni.com/platform/developer/api_explorer")
        bSizer4.Add( self.link, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        bSizer3.Add(bSizer4)
        #Addint text box to size
        self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_textCtrl1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #Adding the button to size
        self.m_button11 = wx.Button( self, wx.ID_ANY, u"Introduce", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_button11, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #Seeting the size and final operations
        self.SetSizer( bSizer3 )
        self.Layout()
        self.Centre( wx.BOTH )
        # Connect Events
        self.m_button11.Bind( wx.EVT_BUTTON, self.OnIntroducingKey )
    def __del__( self ):
        pass
    # Virtual event handlers, overide them in your derived class
    def OnIntroducingKey( self, event ):
        '''
        Accept introducing the key and executing the next steps
        '''
        #We get the value from the input
        geni_key = self.m_textCtrl1.GetValue()
        pub.sendMessage('geni.key.send', geni_key_updated = geni_key)
        self.Close(force=False)
        event.Skip()