'''
Created on 13 ago. 2017

@author: Val
'''
from pyGenealogy.gen_utils import checkDateConsistency
from pyGenealogy import VALUES_ACCURACY

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
        #Birth info
        self.birth_date = ""
        self.accuracy_birth_date = ""
        self.birth_place = ""
        #Death info
        self.death_date = ""
        self.death_place = ""
        self.accuracy_death_date = ""
        #Baptism info
        self.baptism_date = ""
        self.baptism_place = ""
        self.accuracy_baptism_date = ""
        #Residence info
        self.residence_date = ""
        self.residence_place = ""
        self.accuracy_residence_date = ""
        #Burial info
        self.burial_date = ""
        self.burial_place = ""
        self.accuracy_burial_date = ""
        #Marriage info
        self.marriage_date = ""
        self.accuracy_marriage_date = ""
        #Other info
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
        if (not self.selfcheckDateConsistency(birth_date = birth_date, accuracy_birth = accuracy)):
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
        if (not self.selfcheckDateConsistency(death_date = death_date, accuracy_death = accuracy)): 
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
        if (not self.selfcheckDateConsistency(baptism_date = baptism_date, accuracy_baptism = accuracy)):
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
        if (not self.selfcheckDateConsistency(residence_date = residence_date, accuracy_residence = accuracy)):
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
        if (not self.selfcheckDateConsistency(burial_date = burial_date, accuracy_burial = accuracy)):
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
    def selfcheckDateConsistency(self, birth_date = None, residence_date = None, baptism_date = None, 
            marriage_date = None, death_date = None, burial_date = None,
            accuracy_birth = None, accuracy_residence = None, accuracy_baptism = None, 
            accuracy_marriage= None , accuracy_death = None, accuracy_burial = None):
        if (birth_date == None): birth_date = self.birth_date
        if (residence_date == None) : residence_date = self.residence_date
        if (baptism_date == None) : baptism_date = self.baptism_date
        if (marriage_date == None) : marriage_date = self.marriage_date
        if (death_date == None) : death_date = self.death_date
        if (burial_date == None) : burial_date = self.burial_date
        if (accuracy_birth == None) : accuracy_birth = self.accuracy_birth_date
        if (accuracy_residence == None) : accuracy_residence = self.accuracy_residence_date
        if (accuracy_baptism == None) : accuracy_baptism = self.accuracy_baptism_date
        if (accuracy_marriage == None) : accuracy_marriage = self.accuracy_marriage_date
        if (accuracy_death == None) : accuracy_death = self.accuracy_death_date
        if (accuracy_burial == None) : accuracy_burial = self.accuracy_burial_date
        return checkDateConsistency(birth_date, residence_date, baptism_date, 
                         marriage_date, death_date, burial_date,
                         accuracy_birth, accuracy_residence, accuracy_baptism , 
                         accuracy_marriage , accuracy_death, accuracy_burial)