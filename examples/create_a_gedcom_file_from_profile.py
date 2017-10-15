'''
Created on 16 oct. 2017

@author: Val

This example creates a profile, converts into GEDCOM format and builds it

'''

from pyGenealogy.common_profile import gen_profile
from pyGedcom.gedcom_profile import gedcom_profile
from pyGedcom.gedcompy_wrapper import gedcom_file

#Standard creation of a profile
profile = gen_profile("John", "Smith")
#Profile is converted into a profile prepared for gedcom
gedcom_profile.convert_gedcom(profile)
#We create the new gedcom file and we add the new profile
new_gedcom = gedcom_file()
new_gedcom.add_element(profile.individual)
#If you want to save the file...
new_gedcom.save("myoutput.ged")
