'''
Created on 14 oct. 2017

@author: Val

This profile will be use to interact with the GEDCOM file generator.
'''
from pyGenealogy import common_profile
import gedcom

EQUIVALENCE_PROFILE = {"birth" : "BIRT", "death" : "DEAT", "baptism" : "BAPM", "burial" : "BURI"}
EQUIVALENCE = EQUIVALENCE_PROFILE
EQUIVALENCE["marriage"] = "MARR"
LOCATION_EQUIVALENCE = {"city" : "CITY", "state": "STAE", "country" : "CTRY"}

class gedcom_profile(common_profile.gen_profile):
    '''
    Profile derivated from the generic common-profile
    '''


    def __init__(self, individual):
        '''
        Constructor
        '''
        name = ""
        surname = ""
        self.individual = individual
        for data in individual.get_list("NAME"):
            for names in data.get_list("GIVN"):
                name = names.value
            for surnames in data.get_list("SURN"):
                surname = surnames.value
        common_profile.gen_profile.__init__(self, name, surname)
    
    @classmethod
    def convert_gedcom(cls, base_profile):
        '''
        Simply converts into this profile type
        '''
        #Calling essentially the constructors
        if isinstance(base_profile, list):
            for profile in base_profile:
                profile.__class__ = cls
                profile.individual = cls.return_individual_gedcom(profile)
        else:
            base_profile.__class__ = cls
            base_profile.individual = cls.return_individual_gedcom(base_profile)
    
    def return_id(self):
        '''
        This function will return the id of the profile
        '''
        return self.individual.__dict__["id"]
    
    def return_individual_gedcom(self):
        '''
        This function will return the gedcom type individual
        '''
        individual = gedcom.Individual()
        if "gender" in self.gen_data.keys():
            sex = gedcom.Element(tag="SEX", value=self.gen_data["gender"])
            individual.add_child_element(sex)
        name = gedcom.Element(tag="NAME", value=(self.gen_data["name"] + "/" + self.gen_data["surname"] + "/"))
        name_given = gedcom.Element(tag="GIVN", value=self.gen_data["name"])
        name_surname = gedcom.Element(tag="SURN", value=self.gen_data["surname"])
        nick = ""
        for nickname in self.gen_data.get("nicknames", None):
            if nick != "" : nick += ","
            nick += nickname
        name.add_child_element(name_given)
        name.add_child_element(name_surname)
        if (nick != ""):
            name_nickname = gedcom.Element(tag="NICK", value=nick)
            name.add_child_element(name_nickname)
        individual.add_child_element(name)
        
        for date_key in EQUIVALENCE.keys():
            include_date, ged_event = self.get_event_element(date_key)
            if include_date : individual.add_child_element(ged_event)
        return individual
    
    def get_event_element(self, date_key):
        '''
        Function that provides the event value as an element
        '''
        date = self.gen_data.get(common_profile.ALL_EVENT_DATA[date_key]["date"], None)
        accuracy = self.gen_data.get(common_profile.ALL_EVENT_DATA[date_key]["accuracy"], None)
        include_date = False
        ged_event = gedcom.Element(tag=EQUIVALENCE[date_key], value="")
        #Ok, we have a date defined, let's create the relevant element
        if (date):
            include_date = True
            ged_date_string = ""
            full_date =  date.strftime("%d %b %Y").upper()
            if accuracy == "ABOUT":
                ged_date_string = "ABT " + str(date.year)
            elif accuracy == "EXACT":
                ged_date_string = full_date
            elif accuracy == "BEFORE" :
                ged_date_string = "BEF " + full_date
            elif accuracy == "AFTER" :
                ged_date_string = "AFT " + full_date
            ged_date = gedcom.Element(tag="DATE", value=ged_date_string)
            ged_event.add_child_element(ged_date)
                    
        location = self.gen_data.get(common_profile.ALL_EVENT_DATA[date_key]["location"], {})
        if (any(location)):
            include_date = True
            ged_loc = gedcom.Element(tag="ADDR", value="")
            if "raw" in location.keys():
                ged_event_plac = gedcom.Element(tag="PLAC", value=location["raw"])
                ged_event.add_child_element(ged_event_plac)
            for loc_key in LOCATION_EQUIVALENCE.keys():
                #Ok, this data is available, let's use it!
                if loc_key in location.keys():
                    ged_new_loc_data = gedcom.Element(tag=LOCATION_EQUIVALENCE[loc_key], value=location[loc_key])
                    ged_loc.add_child_element(ged_new_loc_data)
            ged_event.add_child_element(ged_loc)
        return include_date, ged_event
        