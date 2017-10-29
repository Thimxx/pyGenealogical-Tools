'''
Created on 12 ago. 2017

@author: Val
'''
import wx
from geniApp.data_storing import StoringKeys
from pyGeni.geniapi_common import geni_calls
from pyGeni import set_token
from wx.lib.pubsub import pub

class AppGeni(wx.App):
    def OnInit(self):
        self.app_data = StoringKeys()
        self.valid_key = False
        self.__runvalidation()
        pub.subscribe(self.__onGeniKeyUpdate, 'geni.key.send')
        return True
    def provide_validation_key(self):
        return self.valid_key
    def __runvalidation(self):
        validator = geni_calls()
        self.valid_key = validator.check_valid_genikey()

    def __onGeniKeyUpdate(self, geni_key_updated):
        '''
        This is a listener that will introduce data
        '''
        self.app_data.setGENIkey(geni_key_updated)
        set_token(geni_key_updated)
        self.__runvalidation()
        pub.sendMessage('geni.key.validate', validation_status = self.valid_key)