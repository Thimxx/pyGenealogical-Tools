'''
Created on 13 ago. 2017

@author: Val
'''
from pyGenealogy.gen_utils import checkDateConsistency, get_score_compare_names, get_score_compare_dates
from pyGenealogy import VALUES_ACCURACY, EVENT_TYPE
from pyGenealogy.gen_utils import get_splitted_name_from_complete_name, LOCATION_KEYS, formated_year
from pyGenealogy.common_event import event_profile

TOOL_ID = "PY-GENEALOGY"
DATA_STRING = ["name", "surname", "name_to_show", "gender", "comments", "id", "marriage_link"]
MERGE_EVENTS = ["birth", "death", "baptism",  "burial", "marriage"]
DATA_ACCURACY = ["accuracy_birth_date", "accuracy_death_date", "accuracy_baptism_date", "accuracy_residence_date", "accuracy_burial_date", "accuracy_marriage_date"]
DATA_PLACES = ["birth_place", "death_place", "baptism_place", "residence_place", "burial_place", "marriage_place"]
DATA_LISTS = ["web_ref", "nicknames"]

EVENT_DATA = {"birth" : {"date":"birth_date", "accuracy": "accuracy_birth_date", "location": "birth_place" },
                   "death" : {"date":"death_date", "accuracy": "accuracy_death_date", "location": "death_place" },
                   "baptism" : {"date":"baptism_date", "accuracy": "accuracy_baptism_date", "location": "baptism_place" },
                   "burial" : {"date":"burial_date", "accuracy": "accuracy_burial_date", "location": "burial_place"}
                   }

EVENT_MARRIAGE = {"marriage" : {"date":"marriage_date", "accuracy": "accuracy_marriage_date", "location": "marriage_place" }}
EVENT_RESIDENCE = {"residence" : {"date":"residence_date", "accuracy": "accuracy_residence_date", "location": "residence_place" }}
ALL_EVENT_DATA = dict(EVENT_DATA)
ALL_EVENT_DATA.update(EVENT_MARRIAGE)
ALL_EVENT_DATA.update(EVENT_RESIDENCE)

ALL_DATA = DATA_STRING + DATA_LISTS + EVENT_TYPE

class gen_profile(object):
    '''
    This class will include a single genealogical profile common for all tools,
    common information like birth dates, death dates... will be covered here.
    '''
    def __init__(self, name, surname, name2show=None):
        '''
        Constructor, name and surname as minimal parameters
        '''
        self.gen_data = {}
        self.gen_data["id"] = None
        self.gen_data["name"] = name
        self.gen_data["surname"] = surname
        self.gen_data["name_to_show"] = self.set_name_2_show(name2show)
        self.gen_data["web_ref"] = []
        self.gen_data["nicknames"] = []
    def add_nickname(self, nick_name):
        '''
        Add a nickname
        '''
        self.gen_data["nicknames"].append(nick_name)
    def set_id(self, id_profile):
        """
        Introduce an id for later on compare the data for introduction
        """
        self.gen_data["id"] = TOOL_ID + str(id_profile)
    def set_marriage_id_link(self, id_partner):
        """
        Sets the link to the id of the partner
        """
        self.gen_data["marriage_link"] =  id_partner
    def set_name(self,name):
        '''
        Modifies name to show
        '''
        self.gen_data["name"] = name
        self.gen_data["name_to_show"] = self.set_name_2_show(None)
    def set_surname(self, surname):
        '''
        Modified name to show as well
        '''
        self.gen_data["surname"] = surname
        self.gen_data["name_to_show"] = self.set_name_2_show(None)
    def set_name_2_show(self, name2show):
        '''
        Setting the name to be shown if not existing
        '''
        if (name2show == None):
            return self.returnFullName()
        else:
            return name2show
    def returnFullName(self):
        return self.getName() + " " + self.getSurname()
    def setCheckedGender(self, gender):
        '''
        This function will set up the gender of the profile, only the following values
        are available:
        M = Male
        F = Female
        U = Unknown
        Returns a True if the value has been properly introduced, and False if the value
        is not correct
        '''
        if(gender == "M" or gender == "F" or gender == "U"):
            self.gen_data["gender"] = gender
            return True
        else:
            return False
    def setCheckedDate(self, event_name, year, month = None, day = None, accuracy = "EXACT", year_end = None,
                month_end = None, day_end = None):
        '''
        This function will introduce an event with the data related to the dates of the event
        '''
        if (not event_name in EVENT_TYPE) or (not accuracy in VALUES_ACCURACY): return False
        new_event = event_profile(event_name)
        new_event.setDate(year, month, day, accuracy, year_end, month_end, day_end)
        if (not self.selfcheckDateConsistency(new_event)):
            return False
        else:
            if event_name in self.gen_data.keys():
                self.gen_data[event_name].setDate(year, month, day, accuracy, year_end, month_end, day_end)
            else:
                self.gen_data[event_name] = new_event
            return True
    def setCheckedDateWithDates(self, event_name, date1, accuracy= "EXACT", date2 = None):
        '''
        This function will allow easy transition to the new function for allowing simple transfer of data with date
        function
        '''
        if date2:
            self.setCheckedDate(event_name, date1.year, month = date1.month, day = date1.day, accuracy = accuracy,
                year_end = date2.year ,month_end = date2.month, day_end = date2.day)
        else:
            self.setCheckedDate(event_name, date1.year, month = date1.month, day = date1.day, accuracy = accuracy,
                year_end = None, month_end = None, day_end = None)
    def setNewEvent(self,event):
        '''
        When the event is already available there is no need to perform the checked date, we just include the event
        '''
        if (not self.selfcheckDateConsistency(event)):
            return False
        else:
            self.gen_data[event.get_event_type()] = event
    def setComments(self, comment):
        '''
        Comments are aditive on top of the preivous one
        '''
        if (not "comments" in self.gen_data.keys()):
            self.gen_data["comments"] = ""
        self.gen_data["comments"] = self.getComments() + comment
    def nameLifespan(self):
        '''
        Function for printing an standard format of naming
        '''
        year_birth = "?"
        if("birth" in self.gen_data.keys()): year_birth = formated_year(self.gen_data["birth"].get_year(), self.gen_data["birth"].get_accuracy())
        year_death = "?"
        if("death" in self.gen_data.keys()): year_death = formated_year(self.gen_data["death"].get_year(), self.gen_data["death"].get_accuracy())
        if (year_birth == "?") and (year_death == "?"):
            return self.getName2Show()
        else:
            return self.getName2Show() + " (" + year_birth + " - " + year_death + ")"
    def setWebReference(self, address):
        '''
        Includes web references for the profile.
        '''
        if isinstance(address, list):
            self.gen_data["web_ref"] += address
        elif isinstance(address, str):
            self.gen_data["web_ref"].append(address)
    def setPlaces(self, event_name, location, language="en" ):
        '''
        This function will introduce the location related to each event
        '''
        if event_name in EVENT_TYPE:
            new_event = self.gen_data.get(event_name, event_profile(event_name))
            new_event.setLocation(location, language)
            self.gen_data[event_name] = new_event
            return True
        else:
            return False
    def get_earliest_event(self):
        '''
        It will return the earliest event, of course, the birth, but it is already checked,
        for simplicity I will not consider that case
        '''
        earliest_date = None
        for event_key in EVENT_TYPE:
            if event_key in self.gen_data:
                if earliest_date == None:
                    earliest_date = self.gen_data[event_key].get_date()
                elif self.gen_data[event_key].get_date() < earliest_date:
                    earliest_date = self.gen_data[event_key].get_date()
        return earliest_date
    def selfcheckDateConsistency(self, new_event):
        '''
        This function is a wrapper for calling the function of checking dates consistencies
        '''
        all_events = self.getEvents()
        all_events.append(new_event)
        return checkDateConsistency(all_events)
    def comparison_score(self, profile, data_language="en", name_convention="father_surname"):
        '''
        Get the score value in comparison
        '''
        score, factor = get_score_compare_names(self.getName(), self.getSurname(),
                        profile.getName(), profile.getSurname(), language=data_language, convention=name_convention)
        #Comparing gender
        if (self.getGender()) and (profile.getGender()):
            if self.getGender() == profile.getGender():
                score += 0.5
            else:
                factor = 0.5*factor
        for event_name in MERGE_EVENTS:
            if (event_name in self.gen_data.keys()) and (event_name in profile.gen_data.keys()) and self.gen_data[event_name].is_any_date_available() and profile.gen_data[event_name].is_any_date_available():
                score_temp, factor_temp = get_score_compare_dates(self.gen_data[event_name],
                                                              profile.gen_data[event_name] )
                score += score_temp
                factor = factor*factor_temp
        return score, factor
    def merge_profile(self, profile, language="en", convention="father_surname"):
        '''
        This will merge into this profile the information from the attached profile
        it will return True if information is mixed and False if merge is not DivisionImpossible
        '''
        score, factor = self.comparison_score(profile, data_language = language,  name_convention = convention)
        if (score*factor > 2.0):
            #Ok, we consider the size big enough
            for key_data in ALL_DATA:
                if(profile.gen_data.get(key_data, None) != None):
                    #That means we have some data!, exists in the other?
                    if(self.gen_data.get(key_data, None) == None):
                        #So is a new data!
                        self.gen_data[key_data] = profile.gen_data[key_data]
                    else:
                        #We have data in both!
                        if (key_data == "name"):
                            name1 = get_splitted_name_from_complete_name(self.getName(), language=language)
                            name2 = get_splitted_name_from_complete_name(profile.getName(), language=language)
                            if (len(name2) > len(name1)): self.set_name(profile.getName())
                        elif (key_data == "surname"):
                            surname1 = get_splitted_name_from_complete_name(self.getSurname(), language=language)
                            surname2 = get_splitted_name_from_complete_name(profile.getSurname(), language=language)
                            if (len(surname2[0]) > len(surname1[0])): self.set_surname(profile.getSurname())
                        elif (key_data == "comments"):
                            self.gen_data["comments"] += "\n" + profile.gen_data["comments"]
                        elif (key_data in DATA_LISTS):
                            for info in profile.gen_data[key_data]:
                                if info not in self.gen_data[key_data] : self.gen_data[key_data].append(info)
                        elif (key_data in EVENT_TYPE):
                            #Merging the data input
                            event_new = profile.gen_data[key_data]
                            if event_new.get_accuracy() == "EXACT":
                                self.gen_data[key_data].setDate(event_new.get_year(),event_new.get_month(),event_new.get_day(),event_new.get_accuracy())
                            for key_location in LOCATION_KEYS:
                                if event_new.get_location() and (event_new.get_location().get(key_location, None) != None):
                                    if self.gen_data[key_data].get_location() and (self.gen_data[key_data].get_location().get(key_location, None) == None):
                                        self.gen_data[key_data].setParameterInLocation(key_location, profile.gen_data[key_data][key_location])
            return True
        else:
            return False
#===============================================================================
#         GET methods: for compatibility withe RootsMagic profile we shall keep compatibility
#===============================================================================
    def getName(self):
        '''
        Function to get the name
        '''
        return self.gen_data["name"]
    def getSurname(self):
        '''
        Function to return the surname
        '''
        return self.gen_data["surname"]
    def getGender(self):
        '''
        Returns the gender of the profile
        '''
        if "gender" in self.gen_data:
            return self.gen_data["gender"]
        else:
            return None
    def getComments(self):
        '''
        Will return the string with all comments from the profile
        '''
        return self.gen_data["comments"]
    def getName2Show(self):
        '''
        Function that provides back the name to be shown
        '''
        return self.gen_data["name_to_show"]
    def getEvents(self):
        '''
        This function will provide all present events inside the profile
        '''
        all_events = []
        for event_name in EVENT_TYPE:
            if event_name in self.gen_data.keys(): all_events.append(self.gen_data[event_name])
        return all_events
    def get_specific_event(self, event_name):
        '''
        It will return an specific event or None if not present
        '''
        return self.gen_data.get(event_name, None)
    def get_accuracy_event(self, event):
        '''
        It will return the accuracy of an event in the profile
        '''
        return self.get_specific_event(event).get_accuracy()
    def get_location_event(self, event):
        '''
        It will return the location of an event in the profile
        '''
        return self.get_specific_event(event).get_location()
    def get_id(self):
        """
        Returns the profile id.
        """
        return self.gen_data.get("id", None)