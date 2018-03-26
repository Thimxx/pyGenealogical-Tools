'''
Created on 13 ago. 2017

@author: Val
'''
from pyGenealogy.gen_utils import checkDateConsistency, get_formatted_location, get_score_compare_names, get_score_compare_dates
from pyGenealogy import VALUES_ACCURACY
from pyGenealogy.gen_utils import get_splitted_name_from_complete_name, LOCATION_KEYS

TOOL_ID = "PY-GENEALOGY"
DATA_STRING = ["name", "surname", "name_to_show", "gender", "comments", "id", "marriage_link"]
MERGE_DATES = ["birth_date", "death_date", "baptism_date",  "burial_date", "marriage_date"]
DATA_DATES = MERGE_DATES + ["residence_date"]
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

ALL_DATA = DATA_STRING + DATA_DATES + DATA_ACCURACY + DATA_PLACES + DATA_LISTS

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
        return self.gen_data["name"] + " " + self.gen_data["surname"]
    def setCheckedGender(self, gender):
        '''
        This function will set up the gender of the profile, only the following values
        are available:
        M = Male
        F = Female
        Returns a True if the value has been properly introduced, and False if the value
        is not correct
        '''
        if(gender == "M" or gender == "F"):
            self.gen_data["gender"] = gender
            return True
        else:
            return False
    def setCheckedDate(self, date_name, date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.selfcheckDateConsistency({ date_name : date}, {"accuracy_" + date_name : accuracy})) or (not accuracy in VALUES_ACCURACY) or (not date_name in DATA_DATES):
            return False
        else:
            self.gen_data[date_name] = date
            self.gen_data["accuracy_" + date_name] = accuracy
            return True
    def setComments(self, comment):
        '''
        Comments are aditive on top of the preivous one
        '''
        if (not "comments" in self.gen_data.keys()):
            self.gen_data["comments"] = ""
        self.gen_data["comments"] = self.gen_data["comments"] + comment
    def nameLifespan(self):
        '''
        Function for printing an standard format of naming
        '''
        year_birth = "?"
        if("birth_date" in self.gen_data.keys()): year_birth = str(self.gen_data["birth_date"].year)
        year_death = "?"
        if("death_date" in self.gen_data.keys()): year_death = str(self.gen_data["death_date"].year)
        if (year_birth == "?") and (year_death == "?"):
            return self.gen_data["name_to_show"]
        else:
            return self.gen_data["name_to_show"] + " (" + year_birth + " - " + year_death + ")"
    def setWebReference(self, address):
        '''
        Includes web references for the profile.
        '''
        if isinstance(address, list):
            self.gen_data["web_ref"] += address
        elif isinstance(address, str):
            self.gen_data["web_ref"].append(address)
    def setPlaces(self, event_place, location, language="en" ):
        '''
        This function will introduce the location related to each event
        '''
        if event_place in DATA_PLACES:
            location_data = get_formatted_location(location, language)
            self.gen_data[event_place] = location_data
            return True
        else:
            return False
    def selfcheckDateConsistency(self, dict_dates, dict_accuracy):
        #We set the dates received or taken from the profiles
        birth_date = dict_dates.get("birth_date", self.gen_data.get("birth_date", None) )
        residence_date = dict_dates.get("residence_date", self.gen_data.get("residence_date", None) )
        baptism_date = dict_dates.get("baptism_date", self.gen_data.get("baptism_date", None) )
        marriage_date = dict_dates.get("marriage_date", self.gen_data.get("marriage_date", None) )
        death_date = dict_dates.get("death_date", self.gen_data.get("death_date", None) )
        burial_date = dict_dates.get("burial_date", self.gen_data.get("burial_date", None) )
        #Similar attemp using accuracy
        accuracy_birth = dict_accuracy.get("accuracy_birth_date", self.gen_data.get("accuracy_birth_date", None) )
        accuracy_residence = dict_accuracy.get("accuracy_residence_date", self.gen_data.get("accuracy_residence_date", None) )
        accuracy_baptism = dict_accuracy.get("accuracy_baptism_date", self.gen_data.get("accuracy_baptism_date", None) )
        accuracy_marriage = dict_accuracy.get("accuracy_marriage_date", self.gen_data.get("accuracy_marriage_date", None) )
        accuracy_death = dict_accuracy.get("accuracy_death_date", self.gen_data.get("accuracy_death_date", None) )
        accuracy_burial = dict_accuracy.get("accuracy_burial_date", self.gen_data.get("accuracy_burial_date", None) )
        return checkDateConsistency(birth_date, residence_date, baptism_date,
                         marriage_date, death_date, burial_date,
                         accuracy_birth, accuracy_residence, accuracy_baptism,
                         accuracy_marriage , accuracy_death, accuracy_burial)
    def comparison_score(self, profile, data_language="en", name_convention="father_surname"):
        '''
        Get the score value in comparison
        '''
        score, factor = get_score_compare_names(self.gen_data["name"], self.gen_data["surname"],
                        profile.gen_data["name"], profile.gen_data["surname"], language=data_language, convention=name_convention)
        #Comparing gender
        if ("gender" in self.gen_data) and ("gender" in profile.gen_data):
            if self.gen_data["gender"] == profile.gen_data["gender"]:
                score += 0.5
            else:
                factor = 0.5*factor
        for date_id in MERGE_DATES:
            if (date_id in self.gen_data.keys()) and (date_id in profile.gen_data.keys()):
                score_temp, factor_temp = get_score_compare_dates(self.gen_data[date_id],
                                                              self.gen_data["accuracy_" + date_id],
                                                              profile.gen_data[date_id],
                                                              profile.gen_data["accuracy_" + date_id])
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
                            name1 = get_splitted_name_from_complete_name(self.gen_data["name"], language=language)
                            name2 = get_splitted_name_from_complete_name(profile.gen_data["name"], language=language)
                            if (len(name2) > len(name1)): self.gen_data["name"] = profile.gen_data["name"]
                        elif (key_data == "surname"):
                            surname1 = get_splitted_name_from_complete_name(self.gen_data["surname"], language=language)
                            surname2 = get_splitted_name_from_complete_name(profile.gen_data["surname"], language=language)
                            if (len(surname2[0]) > len(surname1[0])): self.gen_data["surname"] = profile.gen_data["surname"]
                        elif (key_data == "comments"):
                            self.gen_data["comments"] += "\n" + profile.gen_data["comments"]
                        elif (key_data in DATA_LISTS):
                            for info in profile.gen_data[key_data]:
                                if info not in self.gen_data[key_data] : self.gen_data[key_data].append(info)
                        elif (key_data in MERGE_DATES):
                            if profile.gen_data[EVENT_DATA[key_data.replace("_date","")]["accuracy"]] == "EXACT":
                                self.gen_data[EVENT_DATA[key_data.replace("_date","")]["accuracy"]] = "EXACT"
                                self.gen_data[EVENT_DATA[key_data.replace("_date","")]["date"]] = profile.gen_data[EVENT_DATA[key_data.replace("_date","")]["date"]]
                        elif (key_data in DATA_PLACES):
                            for key_location in LOCATION_KEYS:
                                if profile.gen_data[key_data].get(key_location, None) != None:
                                    if self.gen_data[key_data].get(key_location, None) == None:
                                        self.gen_data[key_data][key_location] = profile.gen_data[key_data][key_location]
            return True
        else:
            return False