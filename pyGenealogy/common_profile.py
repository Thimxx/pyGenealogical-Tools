'''
Created on 13 ago. 2017

@author: Val
'''
from messages.pyGenealogymessages import NO_VALID_BIRTH_DATE, NO_VALID_DEATH_DATE, NO_VALID_DEATH_AND_BURIAL
import logging
from datetime import date

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
        self.accuracy_residence_date = ""
        
        self.burial_date = ""
        self.burial_place = ""
        self.accuracy_burial_date = ""
        
        self.marriage_date = ""
        self.accuracy_marriage_date = ""
        
        self.comments = ""
        
        self.web_ref = []
        
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
        if (not self.checkDateConsistency(birth_date, self.residence_date, self.baptism_date, self.marriage_date, self.death_date, self.burial_date,  
                             accuracy, self.accuracy_residence_date, self.accuracy_baptism_date, 
                             self.accuracy_marriage_date, self.accuracy_death_date, self.accuracy_burial_date)): 
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
        if (not self.checkDateConsistency(self.birth_date, self.residence_date, self.baptism_date, self.marriage_date, death_date, self.burial_date,  
                             self.accuracy_birth_date, self.accuracy_residence_date, self.accuracy_baptism_date, 
                             self.accuracy_marriage_date, accuracy, self.accuracy_burial_date)): 
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
        self.death_place = place   
    def setCheckedBaptismDate(self, baptism_date, accuracy = "EXACT"):
        '''
        Introducing the baptism date
        '''
        if (not self.checkDateConsistency(self.birth_date, self.residence_date, baptism_date, self.marriage_date, self.death_date, self.burial_date, 
                             self.accuracy_birth_date, self.accuracy_residence_date, accuracy, 
                             self.accuracy_marriage_date, self.accuracy_death_date, self.accuracy_burial_date)): 
            return False
        if (accuracy in VALUES_ACCURACY):
            self.baptism_date = baptism_date
            self.accuracy_baptism_date = accuracy
            return True
        else:
            return False
    def setBaptismPlace(self, place):
        '''
        Birth place will be a place introduction of data in a list
        '''
        self.baptism_place = place  
    def setCheckedResidenceDate(self, residence_date, accuracy = "EXACT"):
        '''
        Input shall be a datetime.date format
        '''
        if (not self.checkDateConsistency(self.birth_date, residence_date, self.baptism_date, self.marriage_date, self.death_date, self.burial_date,
                             self.accuracy_birth_date, accuracy, self.accuracy_baptism_date, 
                             self.accuracy_marriage_date, self.accuracy_death_date, self.accuracy_burial_date)): 
            return False
        if (accuracy in VALUES_ACCURACY):
            self.residence_date = residence_date
            self.accuracy_residence_date = accuracy
            return True
        else:
            return False
    def setResidencePlace(self, place):
        '''
        Birth place will be a place introduction of data in a list
        '''
        self.residence_place = place    
    def setCheckedBurialDate(self, burial_date, accuracy = "EXACT"):
        '''
        Introducing the baptism date
        '''
        if (not self.checkDateConsistency(self.birth_date, self.residence_date, self.baptism_date, self.marriage_date, self.death_date, burial_date, 
                             self.accuracy_birth_date, self.accuracy_residence_date, self.accuracy_baptism_date, 
                             self.accuracy_marriage_date, self.accuracy_death_date, accuracy)):
            return False
        if (accuracy in VALUES_ACCURACY):
            self.burial_date = burial_date
            self.accuracy_burial_date = accuracy
            return True
        else:
            return False
    def setBurialPlace(self, place):
        '''
        Birth place will be a place introduction of data in a list
        '''
        self.burial_place = place  
    def checkDateConsistency(self, birth_date, residence_date, baptism_date, marriage_date, death_date, burial_date,
                             accuracy_birth = "EXACT", accuracy_residence = "EXACT", accuracy_baptism = "EXACT", 
                             accuracy_marriage = "EXACT", accuracy_death = "EXACT", accuracy_burial = "EXACT"):
        '''
        Checker of the different dates are consistent
        '''
        #birth date is always the earliest date
        dates_death_check = []
        dates_birth_check = []
        burial_death = []
        #If there is no birth date included there is no need for the check
        if (birth_date != ""):
            dates_birth_check.append(birth_date)
            check_dates_in_birth = [residence_date, baptism_date, marriage_date, death_date, burial_date]
            accuracy_in_birth = [accuracy_residence, accuracy_baptism, accuracy_marriage, accuracy_death, accuracy_burial]
            for index in range(0, len(check_dates_in_birth)):
                if (check_dates_in_birth[index] != ""):
                    if (accuracy_in_birth[index] == "ABOUT"):
                        #If we have an "about" the event has been around that year, with some margin, in this case, we just include
                        #the last date of the year for the check
                        dates_birth_check.append(date(check_dates_in_birth[index].year,12,31))
                    else:
                        dates_birth_check.append(check_dates_in_birth[index])
            #Now we check here the data consistency
            if(min(dates_birth_check) < birth_date):
                logging.error(NO_VALID_BIRTH_DATE) 
                return False
        
        #Burial and Death dates are the latests ones
        if (burial_date != ""): 
            if (accuracy_burial == "ABOUT"):
                burial_death.append(date(burial_date.year,12,31))
            else:
                burial_death.append(burial_date)
        if (death_date != ""):
            intermediate_death = death_date  
            if (accuracy_burial == "ABOUT"):
                intermediate_death = date(death_date.year,12,31)
            burial_death.append(intermediate_death)
            #Burial is never before than death date... unless in vampires, but out of scope
            if (intermediate_death > min(burial_death)):
                logging.error(NO_VALID_DEATH_AND_BURIAL) 
                return False
        
        if ( len(burial_death) > 0):
            check_dates_in_db = [residence_date, baptism_date, marriage_date]
            accuracy_in_db = [accuracy_residence, accuracy_baptism, accuracy_marriage]
            for index in range(0, len(check_dates_in_db)):
                if (check_dates_in_db[index] != ""):
                    if (accuracy_in_db[index] == "ABOUT"):
                        #If we have an "about" the event has been around that year, with some margin, in this case, we just include
                        #the first date of the  year
                        dates_death_check.append(date(check_dates_in_db[index].year,1,1))
                    else:
                        dates_death_check.append(check_dates_in_db[index])
            #Now we check here the data consistency
            if (len(dates_death_check) > 0):
                if (max(dates_death_check) > max(burial_death)):
                    logging.error(NO_VALID_DEATH_DATE) 
                    return False
        return True
    def setComments(self, comment):
        '''
        Comments are aditive on top of the preivous one
        '''
        self.comments = self.comments + comment
    def setWebReference(self, address):
        '''
        Includes web references for the profile.
        '''
        self.web_ref.append(address)
        