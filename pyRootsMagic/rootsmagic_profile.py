'''
Created on 7 jul. 2019

@author: Val
'''
from pyGenealogy import common_profile
from datetime import date

DATE_EVENT_ID = {"birth_date" : "1", "death_date" : "2", "baptism_date" : "3",  "burial_date" : "4"}

class rootsmagic_profile(common_profile.gen_profile):
    '''
    classdocs
    '''
    def __init__(self, name, surname, rm_id, owner_id, database):
        '''
        Constructor
        '''
        self.rm_id = rm_id
        self.owner_id = owner_id
        self.database = database
        common_profile.gen_profile.__init__(self, name, surname)
    def getDate(self, date_name):
        '''
        This function will provide the date and related event data of the date
        by looking to the database for this specific data
        '''
        events = self.database.execute("SELECT * FROM EventTable WHERE OwnerId=" + str(self.owner_id) + " AND  EventType=" +
                                       DATE_EVENT_ID[date_name])
        
        date_data = events.fetchone()
        if date_data: 
            #TODO: everything down here will require update with the new data model
            accuracy = "EXACT"
            if date_data[7][1] == "B":
                accuracy = "BEFORE"
            elif date_data[7][1] == "A":
                accuracy = "AFTER"
            elif date_data[7][12] == "C":
                accuracy = "ABOUT" 
            year = int(date_data[7][3:7])
            month = int(date_data[7][7:9])
            day = int(date_data[7][9:11])
            if month == 0: month = 1
            if day == 0: day = 1
            return date(year, month, day), accuracy
        else: 
            return None, None
    def getGender(self):
        '''
        Method override in order to access directly to the gender of the profile
        '''
        person_info = self.database.execute("SELECT * FROM PersonTable WHERE PersonID=" + str(self.rm_id) )
        person_data = person_info.fetchone()
        if person_data:
            gender = person_data[2]
            if gender == 0: return "M"
            elif gender == 1: return "F"
            else: return "U"