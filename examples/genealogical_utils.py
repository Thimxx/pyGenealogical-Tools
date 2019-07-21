'''
Created on 8 oct. 2017

@author: Val

This example will show how to use several  common genealogical tools that can be used.

All these functionalities are independent of the rest of the code
'''
from pyGenealogy.gen_utils import checkDateConsistency, getBestDate, get_formatted_location, get_name_surname_from_complete_name
from datetime import date
from pyGenealogy.common_event import event_profile

all_events = []

birth_event = event_profile("birth")
birth_event.setDate(1900,1,1)
all_events.append(birth_event)
residence_event = event_profile("residence")
residence_event.setDate(1910,1,1)
all_events.append(residence_event)
baptism_event = event_profile("baptism")
baptism_event.setDate(1901,1,12)
all_events.append(baptism_event)
marriage_event = event_profile("marriage")
marriage_event.setDate(1930,6,1)
all_events.append(marriage_event)
death_event = event_profile("death")
death_event.setDate(1970,1,1)
all_events.append(death_event)
burial_event = event_profile("burial")
burial_event.setDate(1970,1,2)
all_events.append(burial_event)

#This function will provide a True if the dates are consistent (i.e. your are not getting baptised before being born of after dying)
checkDateConsistency(all_events)

#This function will provide the best date, taking 2 dates. In the following case, it will take reisdence date as being more accurate
getBestDate(date(1910,2,1), "AFTER",date(1910,5,1), "EXACT")

GENERIC_PLACE_STRING = "Portillo,Valladolid,Castile and Leon,Spain"
#This function provides a generic location in standard location format. It is using MAPBOX API in behind
get_formatted_location(GENERIC_PLACE_STRING)

my_name = "John Smith"
#It splits a given name into the name and surname. It checks the data with a database of names and surnames.
name, surname = get_name_surname_from_complete_name(my_name, language = "en")