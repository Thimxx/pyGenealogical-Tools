'''
Created on 13 ago. 2017

@author: Val
'''
from messages.pyGenealogymessages import NO_VALID_BIRTH_DATE, NO_VALID_DEATH_DATE
import logging

VALUES_ACCURACY = ["EXACT", "BEFORE", "AFTER", "ABOUT"]

class gen_profile(object):
    '''
    This class will include a single genealogical profile common for all tools,
    common information like birth dates, death dates... will be covered here.
    '''


    def __init__(self, name, surname):
        '''
        Constructor, name and surname as minimal parameters
        '''
        self.name = name
        self.surname = surname
        
        self.gender = ""
        
        self.birth_date = ""
        self.accuracy_birth_date = ""
        self.birth_place = ""
        
        self.death_date = ""
        self.death_place = ""
        self.accuracy_death_date = ""
        
        self.baptism_date = ""
        self.baptism_place = ""
        self.accuracy_baptism_date = ""
        
        self.residence_date = ""
        self.residence_place = ""
        self.burial_date = ""
        self.burial_place = ""
        
        self.marriage_date = ""
        
        self.comments = ""
        
    def returnFullName(self):
        return self.name + " " + self.surname
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
            self.gender = gender
            return True
        else:
            return False
            
    def setCheckedBirthDate(self, birth_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.checkDateConsistency(birth_date, self.baptism_date, self.marriage_date, self.death_date)):
            return False
        if (accuracy in VALUES_ACCURACY):
            self.birth_date = birth_date
            self.accuracy_birth_date = accuracy
            return True
        else:
            return False
    def setBirthPlace(self, place):
        '''
        Birth place will be a place introduction of data in a list
        '''
        self.birth_place = place
    def setCheckedDeathDate(self, death_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.checkDateConsistency(self.birth_date, self.baptism_date, self.marriage_date, death_date)):
            return False
        if (accuracy in VALUES_ACCURACY):
            self.death_date = death_date
            self.accuracy_death_date = accuracy
            return True
        else:
            return False
    def setDeathPlace(self, place):
        '''
        Birth place will be a place introduction of data in a list
        '''
        self.deat_place = place   
    def setCheckedBaptismDate(self, baptism_date, accuracy = "EXACT"):
        '''
        Introducing the baptism date
        '''
        if (not self.checkDateConsistency(self.birth_date, baptism_date, self.marriage_date, self.death_date)):
            return False
        if (accuracy in VALUES_ACCURACY):
            self.baptism_date = baptism_date
            self.accuracy_baptism_date = accuracy
            return True
        else:
            return False
    def checkDateConsistency(self, birth_date, baptism_date, marriage_date, death_date):
        '''
        Checker of the different dates are consistent
        '''
        #birth date is always the earliest date
        dates = []
        for mytime in [birth_date, baptism_date, marriage_date, death_date]:
            if (mytime != ""):
                dates.append(mytime)
        if (birth_date != ""):
            if (min(dates) < birth_date):
                logging.error(NO_VALID_BIRTH_DATE) 
                return False
        if (death_date != ""):
            if (max(dates) > death_date):
                logging.error(NO_VALID_DEATH_DATE) 
                return False
        return True
        