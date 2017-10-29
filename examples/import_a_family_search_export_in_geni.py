'''
Created on 10 sept. 2017

@author: Val

This example takes an export from Family search in excel format. This export
shall be the children of an specific profile.
The inputs needed are:

- The address of one of the parents of the profile.
- The address of both profiles if the previous profile has 2 marriages (ideally select the profile with a single marriage)
- The Token for geni.

Obtain the token in this webpage:

https://www.geni.com/platform/developer/api_explorer

'''

from pyFS.pyfs_open_xlsx import getFSfamily


my_file = "ENTER HERE THE LOCATION OF YOUR FILE"
my_token = "INTRODUCE THE OBTAINED TOKEN"
parent_profile = "INTRODUC THE HTTP ADDRESS OF THE PARENT PROFILE IF HAS A UNIQUE MARRIAGE"

family = getFSfamily(my_file)
family.create_profiles_in_Geni( my_token, parent_profile)
