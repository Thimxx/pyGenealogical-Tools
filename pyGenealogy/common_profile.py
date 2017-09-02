'''
Created on 13 ago. 2017

@author: Val
'''
from pyGenealogy.gen_utils import checkDateConsistency, get_formatted_location
from pyGenealogy import VALUES_ACCURACY

DATA_STRING = ["name", "surname", "name_to_show", "gender", "comment"]
DATA_DATES = ["birth_date", "death_date", "baptism_date", "residence_date", "burial_date", "marriage_date"]
DATA_ACCURACY = ["accuracy_birth_date", "accuracy_death_date", "accuracy_baptism_date", "accuracy_residence_date", "accuracy_burial_date", "accuracy_marriage_date"]
DATA_PLACES = ["birth_place", "death_place", "baptism_place", "residence_place", "burial_place", "marriage_place"]
DATA_LISTS = ["web_ref"]

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
        self.gen_data["name"] = name
        self.gen_data["surname"] = surname
        self.gen_data["name_to_show"] = self.set_name_2_show(name2show)
        self.gen_data["web_ref"] = []
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
    def setCheckedBirthDate(self, birth_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.selfcheckDateConsistency(birth_date = birth_date, accuracy_birth = accuracy)) or (not accuracy in VALUES_ACCURACY):
            return False
        else:
            self.gen_data["birth_date"] = birth_date
            self.gen_data["accuracy_birth_date"] = accuracy
            return True
    def setCheckedDeathDate(self, death_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.selfcheckDateConsistency(death_date = death_date, accuracy_death = accuracy)) or (not accuracy in VALUES_ACCURACY):
            return False
        else:
            self.gen_data["death_date"] = death_date
            self.gen_data["accuracy_death_date"] = accuracy
            return True
    def setCheckedBaptismDate(self, baptism_date, accuracy = "EXACT"):
        '''
        Introducing the baptism date
        '''
        if (not self.selfcheckDateConsistency(baptism_date = baptism_date, accuracy_baptism = accuracy)) or (not accuracy in VALUES_ACCURACY):
            return False
        else:
            self.gen_data["baptism_date"] = baptism_date
            self.gen_data["accuracy_baptism_date"] = accuracy
            return True
    def setCheckedResidenceDate(self, residence_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.selfcheckDateConsistency(residence_date = residence_date, accuracy_residence = accuracy)) or (not accuracy in VALUES_ACCURACY):
            return False
        else:
            self.gen_data["residence_date"] = residence_date
            self.gen_data["accuracy_residence_date"] = accuracy
            return True
    def setCheckedBurialDate(self, burial_date, accuracy = "EXACT"):
        '''
        Introducing the baptism date
        '''
        if (not self.selfcheckDateConsistency(burial_date = burial_date, accuracy_burial = accuracy)) or (not accuracy in VALUES_ACCURACY):
            return False
        else:
            self.gen_data["burial_date"] = burial_date
            self.gen_data["accuracy_burial_date"] = accuracy
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
        self.gen_data["web_ref"].append(address)
    def setPlaces(self, event_place, location, language="en" ):
        '''
        This function will introduce the location related to each event
        '''
        if event_place in DATA_PLACES:
            location_data = get_formatted_location(location, language)
            if (location_data == None): 
                return False
            else:
                self.gen_data[event_place] = location_data
                return True
        else:
            return False
    def selfcheckDateConsistency(self, birth_date = None, residence_date = None, baptism_date = None, 
            marriage_date = None, death_date = None, burial_date = None,
            accuracy_birth = None, accuracy_residence = None, accuracy_baptism = None, 
            accuracy_marriage= None , accuracy_death = None, accuracy_burial = None):
        if (birth_date == None): birth_date = self.gen_data.get("birth_date", None)
        if (residence_date == None) : residence_date = self.gen_data.get("residence_date", None)
        if (baptism_date == None) : baptism_date = self.gen_data.get("baptism_date", None)
        if (marriage_date == None) : marriage_date = self.gen_data.get("marriage_date", None)
        if (death_date == None) : death_date = self.gen_data.get("death_date", None)
        if (burial_date == None) : burial_date = self.gen_data.get("burial_date", None)
        if (accuracy_birth == None) : accuracy_birth = self.gen_data.get("accuracy_birth_date", None)
        if (accuracy_residence == None) : accuracy_residence = self.gen_data.get("accuracy_residence_date", None)
        if (accuracy_baptism == None) : accuracy_baptism = self.gen_data.get("accuracy_baptism_date", None)
        if (accuracy_marriage == None) : accuracy_marriage = self.gen_data.get("accuracy_marriage_date", None)
        if (accuracy_death == None) : accuracy_death = self.gen_data.get("accuracy_death_date", None)
        if (accuracy_burial == None) : accuracy_burial = self.gen_data.get("accuracy_burial_date", None)
        return checkDateConsistency(birth_date, residence_date, baptism_date, 
                         marriage_date, death_date, burial_date,
                         accuracy_birth, accuracy_residence, accuracy_baptism , 
                         accuracy_marriage , accuracy_death, accuracy_burial)