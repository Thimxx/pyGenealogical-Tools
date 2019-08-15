'''
Created on 7 jul. 2019

@author: Val
'''
from pyGenealogy import common_profile
from pyGenealogy.common_event import event_profile
from pyRootsMagic import collate_temp

DATE_EVENT_ID = {"birth" : "1", "death" : "2", "baptism" : "3",  "burial" : "4", "marriage" : "300", "residence" : "29"}

class rootsmagic_profile(common_profile.gen_profile):
    '''
    Profile with direct interface with RootsMagic database
    '''
    def __init__(self, person_id, database):
        '''
        Constructor
        '''
        self.gen_data = {}
        self.set_id(person_id)
        self.database = database
        common_profile.gen_profile.__init__(self, self.getName() , self.getSurname())
#===============================================================================
#         GET methods: same methods as common_profile
#===============================================================================
    def getName(self):
        '''
        We get the name from the name table directly
        '''
        return self.return_person_data_in_NameTable()[0]
    def getSurname(self):
        '''
        Function to return the surname
        '''
        return self.return_person_data_in_NameTable()[1]
    def getGender(self):
        '''
        Method override in order to access directly to the gender of the profile
        '''
        person_data = self.return_person_in_PersonTable()
        if person_data:
            gender = person_data[2]
            if gender == 0: return "M"
            elif gender == 1: return "F"
            else: return "U"
    def getLiving(self):
        '''
        Method override in order to access directly to the gender of the profile
        '''
        person_data = self.return_person_in_PersonTable()
        if person_data:
            living = int(person_data[10])
            if living == 1: return True
            else: return False
#===============================================================================
#    These functions are left in the base function: getComments, getName2Show, get_all_urls
#===============================================================================
    def getEvents(self):
        '''
        This function will provide all present events inside the profile
        '''
        all_events = []
        input_database = "SELECT * FROM EventTable WHERE OwnerId= ?"
        events = self.database.execute(input_database, (str(self.get_id()),) )
        loop_fetch = True
        while loop_fetch:
            this_event = events.fetchone()
            if this_event:
                new_event = self.return_event_from_database_info(this_event)
                if new_event: all_events.append(new_event)
            else:
                loop_fetch = False
                return all_events
    def get_specific_event(self, event_name):
        '''
        This function will provide the date and related event data of the date
        by looking to the database for this specific data
        '''
        input_events = "SELECT * FROM EventTable WHERE OwnerId=? AND  EventType=?"
        events = self.database.execute(input_events, (str(self.get_id()),DATE_EVENT_ID[event_name],) )
        #Now let's fetch the first value
        date_data = events.fetchone()
        if date_data:
            return self.return_event_from_database_info(date_data)
        else:
            return None
    def get_all_webs(self):
        '''
        This function will provide all web references
        '''
        webs = []
        input_urls = "SELECT * FROM URLTable WHERE OwnerID=?"
        url_info = self.database.execute( input_urls, (str(self.get_id()),) ).fetchall()
        for url_data in url_info:
            web_dict = {}
            web_dict["name"] = url_data[4]
            web_dict["url"] = url_data[5]
            web_dict["notes"] = url_data[6]
            webs.append(web_dict)
        fs_urls = "SELECT * FROM LinkTable WHERE rmID=?"
        fs_info = self.database.execute( fs_urls, (str(self.get_id()),) ).fetchall()
        for fs_data in fs_info:
            web_dict = {}
            web_dict["name"] = "FAMILY-SEARCH-LINK"
            web_dict["url"] = "https://www.familysearch.org/tree/person/details/" + fs_data[4]
            webs.append(web_dict)
        return webs
#===============================================================================
#         SET methods: the value of the profile is modified, overwrtting methods
#        from common_profile
#===============================================================================
    def setWebReference(self, url, name=None, notes=None):
        '''
        Includes web references for the profile.
        There are 2 options for introduction:
        - Introduce a list of urls. In that case only the first argument will be considered
        - Introduce a single url, with description of names and notes
        '''
        #If the introduced values is a list of url, name and notes are ignored
        if isinstance(url, list):
            for new_add in url:
                new_web = "INSERT INTO URLTable(OwnerType,LinkType,OwnerID,URL,Name,Note) VALUES(0,0,?,?,?,?)"
                self.database.execute( new_web, (str(self.get_id()), str(new_add), "", "") )
        elif isinstance(url, str):
            value_name = str(name)
            value_notes = str(notes)
            if name == None: value_name = ""
            if notes == None: value_notes = ""
            new_web = "INSERT INTO URLTable(OwnerType,LinkType,OwnerID,URL,Name,Note) VALUES(0,0,?,?,?,?)"
            self.database.execute( new_web, (str(self.get_id()), str(url), value_name, value_notes) )
        self.database.commit()
    def set_task(self, task_details, priority=0, details=""):
        '''
        Introduces a task linked to the given profile
        '''
        empty_value=""
        self.database.create_collation("RMNOCASE", collate_temp)

        new_task = "INSERT INTO ResearchTable(TaskType,OwnerID,OwnerType,RefNumber, Status, Priority, Filename, Name, Details) VALUES(0,?,0,?,0,?,?,?,?)"
        self.database.execute( new_task, (str(self.get_id()),empty_value, str(priority), empty_value, str(task_details), details, ) )
        self.database.create_collation("RMNOCASE", None)
        self.database.commit()
#===============================================================================
#         UPDATE methods: modified inputs which depend on database
#===============================================================================
    def update_web_ref(self, url, name = None, notes = None):
        '''
        This function will update a given web reference
        '''
        #This will mean that exists... so we can continue
        if url in self.get_all_urls():
            if name :
                update_name = "UPDATE URLTable SET Name = ? WHERE URL=? AND OwnerID=?"
                self.database.execute( update_name, (str(name), str(url), str(self.get_id()), ) )
            if notes :
                update_note = "UPDATE URLTable SET Note = ? WHERE URL=? AND OwnerID=?"
                self.database.execute( update_note, (str(notes), str(url), str(self.get_id()), ) )
            self.database.commit()
            return True
        else:
            return None
#===============================================================================
#         Repetitive methods to be used inside the other functions
#===============================================================================
    def return_person_in_PersonTable(self):
        '''
        Common function used to get the table with table of PersonTable used for gender
        '''
        input_person = "SELECT * FROM PersonTable WHERE PersonID=?"
        person_info = self.database.execute( input_person, (str(self.get_id()),) )
        return person_info.fetchone()
    def return_person_data_in_NameTable(self):
        '''
        Common function used to get the table with the NameTable, used for name and surname
        '''
        input_person = "SELECT * FROM NameTable WHERE OwnerID=?"
        name_info = self.database.execute( input_person, (str(self.get_id()),) )
        loop_database = True
        while loop_database:
            name_data = name_info.fetchone()
            if int(name_data[10]) == 1:
                loop_database = False
                return name_data[3],name_data[2]
    def return_event_from_database_info(self, event_in_database):
        '''
        This function is used to get info about all events
        '''
        if not str(event_in_database[1]) in DATE_EVENT_ID.values(): return None
        event_output = event_profile(list(DATE_EVENT_ID.keys())[list(DATE_EVENT_ID.values()).index(str(event_in_database[1]))])
        if not ( (event_in_database[7] in [ "."]) or event_in_database[7].startswith("T") ):
            #This means that the event has a date, as might be empty
            year_end = None
            month_end = None
            day_end = None
            accuracy_value = "EXACT"
            if event_in_database[7][1] == "B":
                accuracy_value = "BEFORE"
            elif event_in_database[7][1] == "A":
                accuracy_value = "AFTER"
            elif event_in_database[7][1] == "R":
                #Only in the case of dates between is when we analyze and define the dates after
                accuracy_value = "BETWEEN"
                year_end = int(event_in_database[7][14:18])
                month_end = int(event_in_database[7][18:20])
                day_end = int(event_in_database[7][20:22])
                if year_end == 0 : year_end = None
                if month_end == 0 : month_end = None
                if day_end == 0 : day_end = None
            elif event_in_database[7][12] == "C":
                accuracy_value = "ABOUT"
            year = int(event_in_database[7][3:7])
            month = int(event_in_database[7][7:9])
            day = int(event_in_database[7][9:11])
            if month == 0: month = None
            if day == 0: day = None
            event_output.setDate(year, month, day, accuracy_value, year_end, month_end, day_end)
        if not event_in_database[5] == 0:
            #The only valid place is actually when is an entry in the PlaceTbale
            place_input = "SELECT * FROM PlaceTable WHERE PlaceID=?"
            place = self.database.execute(place_input, (str(event_in_database[5]), )  )
            place_info = place.fetchone()
            event_output.setLocation(place_info[2])
            if int(place_info[5]) != 0 and int(place_info[6]) != 0:
                event_output.set_geo_location(int(place_info[5])/10000000, int(place_info[6])/10000000)
        return event_output