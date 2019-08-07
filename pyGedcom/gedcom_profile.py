'''
Created on 14 oct. 2017

@author: Val

This profile will be use to interact with the GEDCOM file generator.
'''
from pyGenealogy import common_profile
from pyGedcom import EQUIVALENCE, LOCATION_EQUIVALENCE, get_date_info_from_ged, EQUIVALENCE_PROFILE
from pyGenealogy.common_event import event_profile
from pyGenealogy import EVENT_TYPE
import copy


class gedcom_profile(common_profile.gen_profile):
    '''
    Profile derived from the generic common-profile but using as input the output from the gedcom file
    '''
    def __init__(self, individual = None, name = None, surname = None):
        '''
        Constructor, the input shall be the input dictionary from gedcom
        '''
        if individual:
            self.individual = individual
            #Initiation of constructor, we will set-up the names first
            name = individual.get("NAME", {}).get("GIVN", {}).get("VALUE")
            surname = individual.get("NAME", {}).get("SURN", {}).get("VALUE")
            inter = individual.get("NAME").get("VALUE").split("/")
            #In case that there is not information available, we take the overall one
            if not name: name = inter[0]
            if not surname : surname = inter[1]
        else:
            self.individual = {"VALUE": "INDI"}
            value_name = ""
            self.individual["NAME"] = {}
            if name:
                self.individual["NAME"]["GIVN"] = {"VALUE": name}
                value_name += name
            if surname:
                self.individual["NAME"]["SURN"] = {"VALUE": surname}
                value_name += " / " + surname
            self.individual["NAME"]["VALUE"] = value_name
        common_profile.gen_profile.__init__(self, name, surname)
    @classmethod
    def convert_gedcom(cls, base_profile):
        '''
        Simply converts into this profile type
        '''
        #Calling essentially the constructors
        if isinstance(base_profile, list):
            for profile in base_profile:
                copy_profile = copy.deepcopy(profile)
                profile.__class__ = cls
                profile.individual = cls.return_individual_gedcom(profile, copy_profile)
        else:
            copy_profile = copy.deepcopy(base_profile)
            base_profile.__class__ = cls
            base_profile.individual = cls.return_individual_gedcom(base_profile, copy_profile)
    def return_individual_gedcom(self, copy_profile):
        '''
        This function will return the gedcom type individual
        '''
        individual_gedcom = {"VALUE": "INDI"}
        if "gender" in self.gen_data.keys():
            individual_gedcom["SEX"] = {"VALUE" : copy_profile.getGender()}
        individual_gedcom["NAME"] = { "VALUE" : copy_profile.getName() + "/" + copy_profile.getSurname() + "/",
             "GIVN" :  {"VALUE" : copy_profile.getName()},
             "SURN" :  {"VALUE" : copy_profile.getSurname()},
             }
        #To add potential nicknames
        nick = ""
        for nickname in self.gen_data.get("nicknames", None):
            if nick != "" : nick += ","
            nick += nickname
        if (nick != ""):
            individual_gedcom["NAME"]["NICK"] = {"VALUE" : nick}
        for event in copy_profile.getEvents():
            individual_gedcom[EQUIVALENCE_PROFILE[event.get_event_type()]] = self.extract_gedcom_input_from_gedcom(event)
        return individual_gedcom
    def extract_gedcom_input_from_gedcom(self, event):
        '''
        This function will provide a dictionary input that can be used inside the internal conversions
        '''
        output = {}
        if get_gedcom_formatted_date(event):
            output["DATE"] = { "VALUE" : get_gedcom_formatted_date(event)}
        location = event.get_location()
        if location:
            if "raw" in location.keys(): output["PLAC"] = {"VALUE":location["raw"]}
            if "place_name" in location.keys(): output["PLAC"] = {"VALUE":location["place_name"]}
            for key in LOCATION_EQUIVALENCE.keys():
                if "ADDR" not in output.keys():
                    output["ADDR"] = {}
                if key in location.keys():
                    output["ADDR"][LOCATION_EQUIVALENCE[key]] = {"VALUE" : location[key]}
        return output
#===============================================================================
#         GET methods: for compatibility with Common_profile profile
#        Methods kept original: getName, getSurname, getName2Show, get_accuracy_event, get_location_event
#        Value that will require some thinking: getComments
#===============================================================================
    def getGender(self):
        '''
        Returns the gender of the profile
        '''
        return self.individual.get("SEX", {}).get("VALUE", "U")
    def getEvents(self):
        '''
        This function will provide all present events inside the profile
        '''
        all_events = []
        for event_name in EVENT_TYPE:
            event = self.get_specific_event(event_name)
            if event: all_events.append(event)
        return all_events
    def get_specific_event(self, event_name):
        '''
        It will return an specific event or None if not present
        '''
        if EQUIVALENCE[event_name] in self.individual:
            new_event = event_profile(event_name)
            geddate = self.individual.get(EQUIVALENCE[event_name]).get("DATE", {}).get("VALUE")
            if geddate:
                year, month, day, accuracy, year_end, month_end, day_end = get_date_info_from_ged(geddate)
                new_event.setDate(year, month, day, accuracy, year_end, month_end, day_end)
            if self.individual.get(EQUIVALENCE[event_name]).get("PLAC", {}).get("VALUE"):
                new_event.setParameterInLocation("place_name", self.individual.get(EQUIVALENCE[event_name]).get("PLAC", {}).get("VALUE"))
            for key in LOCATION_EQUIVALENCE:
                if self.individual.get(EQUIVALENCE[event_name]).get("ADDR", {}).get(LOCATION_EQUIVALENCE[key], {}).get("VALUE"):
                    new_event.setParameterInLocation(key, self.individual.get(EQUIVALENCE[event_name]).get("ADDR", {}).get(LOCATION_EQUIVALENCE[key], {}).get("VALUE"))
            return new_event
        else:
            return None
#===============================================================================
#         SET methods: for compatibility with Common_profile profile
#        Only one method has been addressed!!!
#===============================================================================
    def setCheckedDate(self, event_name, year, month = None, day = None, accuracy = "EXACT", year_end = None,
                month_end = None, day_end = None):
        '''
        This function will introduce an event with the data related to the dates of the event
        '''
        value = super().setCheckedDate(event_name, year, month, day, accuracy, year_end,month_end, day_end)
        if value:
            self.individual[EQUIVALENCE_PROFILE[event_name]] = self.extract_gedcom_input_from_gedcom(self.gen_data[event_name])
        return value
    def set_id(self, id_profile):
        """
        The id is introduced, this method should ideally only be used by database
        """
        self.gen_data["id"] = str(id_profile)
#===============================================================================
#         Axuliary functions and methods
#===============================================================================
def get_gedcom_formatted_date(event):
    '''
    This function will provide a formatted date with GEDCOM format
    '''
    ged_date_string = ""
    full_date =  event.get_gedcom_date()
    if full_date:
        if event.get_accuracy() == "ABOUT":
            ged_date_string = "ABT " + full_date
        elif event.get_accuracy() == "EXACT":
            ged_date_string = full_date
        elif event.get_accuracy() == "BEFORE":
            ged_date_string = "BEF " + full_date
        elif event.get_accuracy() == "AFTER":
            ged_date_string = "AFT " + full_date
        elif event.get_accuracy() == "BETWEEN":
            ged_date_string = "BET " + full_date + " AND " + event.get_gedcom_end_date()
        return ged_date_string
    else: return None