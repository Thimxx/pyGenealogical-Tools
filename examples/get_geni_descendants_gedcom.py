'''
Created on 27 mar. 2018

@author: Val

This example shows how to extract a gedcom of descendants of a profile

'''

from pyGeni.profile import profile
from pyGeni import set_token, geni2gedcom

#Very first thing to do is to obtain a Geni key for your app
#go to this location and get:
#https://www.geni.com/platform/developer/api_explorer
GENI_KEY = "IntroduceHereYourGeniKey"
#Introduce here the output file for the gedcom output file
OUTPUT_GEDCOM = "Mylocation.ged"

#First think is to update the GENI_KEY inside the module
set_token(GENI_KEY)
#Select the profile you would like to read in Geni, for example Philip IV king of Spain
profile_web_address = "https://www.geni.com/people/Felipe-IV-el-Grande-rey-de-Espa%C3%B1a-y-Portugal/6000000000837888160"

#We just get the profile
philip = profile(profile_web_address)

#Now we create the class that creates the tree
extractor = geni2gedcom.geni2gedcom(philip)

#Simply execute the extractor.
#Be careful! This example will drive a massive extraction!
extractor.get_gedcom(OUTPUT_GEDCOM)