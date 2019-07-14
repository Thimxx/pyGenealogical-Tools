'''
Created on 8 oct. 2017

@author: Val

This example will show how to use several  common genealogical tools that can be used.

All these functionalities are independent of the rest of the code
'''
from pyGenealogy.gen_utils import checkDateConsistency, getBestDate, get_formatted_location, get_name_surname_from_complete_name
from datetime import date

birth_date = date(1900,1,1)
residence_date = date(1910,1,1)
baptism_date = date(1901,1,12)
marriage_date = date(1930,6,1)
death_date = date(1970,1,1)
burial_date = date(1970,1,2)

#This function will provide a True if the dates are consistent (i.e. your are not getting baptised before being born of after dying)
checkDateConsistency(birth_date, residence_date, baptism_date, marriage_date, death_date, burial_date,
                         accuracy_birth = "EXACT", accuracy_residence = "EXACT", accuracy_baptism = "EXACT",
                         accuracy_marriage = "EXACT", accuracy_death = "EXACT", accuracy_burial = "EXACT")



#This function will provide the best date, taking 2 dates. In the following case, it will take reisdence date as being more accurate
getBestDate(birth_date, "AFTER", residence_date, "EXACT")

GENERIC_PLACE_STRING = "Portillo,Valladolid,Castile and Leon,Spain"
#This function provides a generic location in standard location format. It is using MAPBOX API in behind
get_formatted_location(GENERIC_PLACE_STRING)

my_name = "John Smith"
#It splits a given name into the name and surname. It checks the data with a database of names and surnames.
name, surname = get_name_surname_from_complete_name(my_name, language = "en")