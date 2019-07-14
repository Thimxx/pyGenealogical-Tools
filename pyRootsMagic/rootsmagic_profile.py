'''
Created on 7 jul. 2019

@author: Val
'''
from pyGenealogy import common_profile
from datetime import date
from pyGenealogy.common_event import event_profile

DATE_EVENT_ID = {"birth" : "1", "death" : "2", "baptism" : "3",  "burial" : "4"}

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
    def get_specific_event(self, event_name):
        '''
        This function will provide the date and related event data of the date
        by looking to the database for this specific data
        '''
        events = self.database.execute("SELECT * FROM EventTable WHERE OwnerId=" + str(self.owner_id) + " AND  EventType=" +
                                       DATE_EVENT_ID[event_name])
        
        date_data = events.fetchone()
        if date_data: 
            event_output = event_profile(event_name)
            year_end = None
            month_end = None
            day_end = None
            #TODO: everything down here will require update with the new data model
            accuracy_value = "EXACT"
            if date_data[7][1] == "B":
                accuracy_value = "BEFORE"
            elif date_data[7][1] == "A":
                accuracy_value = "AFTER"
            elif date_data[7][1] == "R":
                #Only in the case of dates between is when we analyze and define the dates after
                accuracy_value = "BETWEEN"
                year_end = int(date_data[7][14:18])
                month_end = int(date_data[7][18:20])
                day_end = int(date_data[7][20:22])
                if year_end == 0 : year_end = None
                if month_end == 0 : month_end = None
                if day_end == 0 : day_end = None
            elif date_data[7][12] == "C":
                accuracy_value = "ABOUT" 
            year = int(date_data[7][3:7])
            month = int(date_data[7][7:9])
            day = int(date_data[7][9:11])
            if month == 0: month = None
            if day == 0: day = None
            event_output.setDate(year, month, day, accuracy_value, year_end, month_end, day_end)
            return event_output
        else: 
            return None
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