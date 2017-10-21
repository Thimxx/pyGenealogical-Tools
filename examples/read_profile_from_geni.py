'''
Created on 24 sept. 2017

@author: Val

This example provides the way to read Geni profiles
'''

from pyGeni.profile import profile
from pyGeni import set_token

#Very first thing to do is to obtain a Geni key for your app
#go to this location and get:
#https://www.geni.com/platform/developer/api_explorer
GENI_KEY = "IntroduceHereYourGeniKey"

#First think is to update the GENI_KEY inside the module
set_token(GENI_KEY)
#Select the profile you would like to read in Geni, for example Philip IV king of Spain
profile_web_address = "https://www.geni.com/people/Felipe-IV-el-Grande-rey-de-Espa%C3%B1a-y-Portugal/6000000000837888160"

#We just get the profile
philip = profile(profile_web_address)