'''
Created on 7 jul. 2019

@author: Val
'''
from pyGenealogy import common_profile
from pyGenealogy.common_event import event_profile
from pyRootsMagic import collate_temp, return_date_from_event, get_geolocated_before, set_geolocated
from messages.py_rootsmagic_messages import WARNING_RESEARCH_LOG, PROFILE_RESEARCH_LOG
from datetime import date, datetime
import logging
from pyGenealogy import NOT_KNOWN_VALUE

DATE_EVENT_ID = {"birth" : "1", "death" : "2", "baptism" : "3",  "burial" : "4", "marriage" : "300", "residence" : "29"}
PERSONAL_EVENTS = ["birth", "death", "baptism", "burial", "residence"]
ARRAY_EVENTS = ["marriage", "residence"]

logger = logging.getLogger('rootsmagic')

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
        name = self.return_person_data_in_NameTable()[0]
        if name == "": return NOT_KNOWN_VALUE
        else: return name
    def getSurname(self):
        '''
        Function to return the surname
        '''
        surname = self.return_person_data_in_NameTable()[1]
        if surname == "": return NOT_KNOWN_VALUE
        else: return surname
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
    def get_nicknames(self):
        '''
        It will go to RootsMagic database and provide all defined nicknames
        '''
        return self.return_person_data_in_NameTable(primary = 0)
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
    def getMarriages(self):
        '''
        It will provide a list of families ID where this profile is parent
        '''
        all_events = []
        #We get all families of the profile first where is parent
        families = ""
        family_id = "SELECT * FROM FamilyTable WHERE FatherID=? OR MotherID=?"
        family_cursor = self.database.execute(family_id, (str(self.get_id()),str(self.get_id()),) )
        #There can be several families
        for family in family_cursor:
            families += str(int(family[0]))
        if families != "":
            #In this case the profile belongs to a family
            input_marriage = "SELECT * FROM EventTable WHERE OwnerType=1 AND OwnerId IN (?)"
            events = self.database.execute(input_marriage, (families,) )
            loop_fetch = True
            while loop_fetch:
                this_event = events.fetchone()
                if this_event:
                    new_event = self.return_event_from_database_info(this_event)
                    if new_event: all_events.append(new_event)
                else:
                    loop_fetch = False
        return all_events
    def getEvents(self):
        '''
        This function will provide all present events inside the profile
        '''
        all_events = self.getMarriages()
        input_database = "SELECT * FROM EventTable WHERE OwnerType=0 AND OwnerId= ?"
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
        if event_name == "marriage": return self.getMarriages()
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
    def get_specific_web(self, web_name):
        '''
        This method will provide an specific web reference defined in the profile
        web_name is an string with the name of the web (not the url)
        '''
        web = {}
        input_urls = "SELECT * FROM URLTable WHERE OwnerID=? AND Name LIKE ?"
        url_info = self.database.execute( input_urls, (str(self.get_id()), web_name, ) ).fetchone()
        if url_info:
            web["name"] = url_info[4]
            web["url"] = url_info[5]
            web["notes"] = url_info[6]
        return web
    def get_specific_research_log(self, log_name):
        '''
        This function will provide an specific log research log in the database, if existing for the owner id
        '''
        self.database.create_collation("RMNOCASE", collate_temp)
        input_rlog = "SELECT * FROM ResearchTable WHERE OwnerId=? AND  Name LIKE ? AND TaskType=2"
        logs = self.database.execute(input_rlog, (str(self.get_id()),str(log_name),) )
        #Now let's fetch the first value
        logs_data = logs.fetchone()
        if len(logs.fetchmany()) > 0:
            logger.warning(WARNING_RESEARCH_LOG + str(log_name) + PROFILE_RESEARCH_LOG + str(self.get_id()))
        else:
            self.database.create_collation("RMNOCASE", None)
        if logs_data:
            return logs_data[0]
        else:
            return None
    def get_all_research_item(self):
        '''
        This function will return all the research logs linked to a given profile
        '''
        items = []
        input_logs = "SELECT * FROM ResearchTable WHERE OwnerID=? AND TaskType=2"
        logs_info = self.database.execute( input_logs, (str(self.get_id()),) ).fetchall()
        #With the following code we will obtain all the research logs in place in the profile
        all_items = []
        for logs in logs_info:
            #Now we will obtain all the inputs inside all research logs
            input_items = "SELECT * FROM ResearchItemTable WHERE LogID=?"
            item_info = self.database.execute( input_items, (str(logs[0]),) ).fetchall()
            all_items += item_info
        #item_info = self.database.execute( input_items ).fetchall()
        for item in all_items:
            web_dict = {}
            web_dict["name"] = item[7]
            web_dict["url"] = item[5]
            web_dict["notes"] = item[8]
            items.append(web_dict)
        return items
    def get_all_tasks(self):
        '''
        This function will return all tasks associated with a given profile
        '''
        input_logs = "SELECT * FROM ResearchTable WHERE OwnerID=? AND TaskType=0"
        logs_info = self.database.execute( input_logs, (str(self.get_id()),) ).fetchall()
        #With the following code we will obtain all the research logs in place in the profile
        all_items = []
        for logs in logs_info:
            task_info = {}
            #Now we will define the task one by one
            task_info["task_details"] = logs[5]
            task_info["priority"] = logs[7]
            task_info["details"] = logs[15]
            all_items.append(task_info)
        return all_items
    def get_source_id_ref(self, name):
        '''
        It will provide back the reference of the source id for internal use
        '''
        source_logs = "SELECT * FROM SourceTable WHERE Name LIKE ?"
        logs_info = self.database.execute( source_logs, (name,) ).fetchone()
        if logs_info: return logs_info[0]
        else: return None
    def get_citation_with_comments(self, comments):
        '''
        It will return, if exists, a citatuion wiht specific comments
        '''
        citation_logs = "SELECT * FROM CitationTable WHERE OwnerID = ? and Comments LIKE ?"
        logs_info = self.database.execute( citation_logs, (str(self.get_id()), comments, ) ).fetchone()
        if logs_info: return logs_info[0]
        else: return None
    def get_place_id_by_name(self, name):
        '''
        Will provide the place id if existing by the name provided
        name will be an string separated by commas
        '''
        input_place = "SELECT * FROM PlaceTable WHERE Name LIKE ?"
        logs_info = self.database.execute( input_place, (name, ) ).fetchall()
        self.database.commit()
        if len(logs_info) > 0: return logs_info[0][0]
        return None
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
            if name is None: value_name = ""
            if notes is None: value_notes = ""
            new_web = "INSERT INTO URLTable(OwnerType,LinkType,OwnerID,URL,Name,Note) VALUES(0,0,?,?,?,?)"
            self.database.execute( new_web, (str(self.get_id()), str(url), value_name, value_notes) )
        self.database.commit()
    def set_task(self, task_details, priority=1, details="", task_type = 0):
        '''
        Introduces a task linked to the given profile
        Task_details: include a list a description of the task or the name of the research log
        Priority: the priority
        Details: the details of the task
        task_type: 0 for a simple item, 2 for a research log
        '''
        empty_value=""
        self.database.create_collation("RMNOCASE", collate_temp)
        new_task = ("INSERT INTO ResearchTable(TaskType,OwnerID,OwnerType,RefNumber, Status, Priority, Filename, Name, Details, Date1, Date2, Date3, SortDate1,"
                    " SortDate2, SortDate3) VALUES(?,?,0,?,0,?,?,?,?,?,?,?,9223372036854775807,9223372036854775807,9223372036854775807)")
        cursor = self.database.cursor()
        cursor.execute( new_task, (str(task_type), str(self.get_id()),empty_value, str(priority), empty_value, str(task_details), details,".", ".", ".", ) )
        row_data = cursor.lastrowid
        self.database.create_collation("RMNOCASE", None)
        self.database.commit()
        return row_data
    def set_research_item(self, log_id, repository = "", source = "", result = ""):
        '''
        This will introduce a new research item inside the given research log
        log_id is the id of the research log that will contain the research item
        repository is the location of the research, like a webpage
        source is the source of hte information
        result is the final outcome
        '''
        #Get the date of today in the form of RootsMagic
        new_event = event_profile("residence")
        today = date.today()
        new_event.setDate(today.year, today.month, today.day, "EXACT")
        date_of_research = return_date_from_event(new_event)
        new_item = "INSERT INTO ResearchItemTable(LogID,Date,Repository,Source,Result) VALUES(?,?,?,?,?)"
        self.database.execute( new_item, (str(log_id), date_of_research, repository, source, result, ) )
        self.database.commit()
    def set_source_id(self, name, isprivate=0, templateID = 144, fields = None):
        '''
        Introduces a new source id inside RootsMagic
        '''
        self.database.create_collation("RMNOCASE", collate_temp)
        if not fields:
            fields = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><Root><Fields><Field><Name>Newspaper</Name><Value>"
            fields += name
            fields += "</Value></Field><Field><Name>TranslatedName</Name><Value/></Field><Field><Name>PubPlace</Name><Value/></Field></Fields></Root>"
        new_item = "INSERT INTO SourceTable(Name, RefNumber, ActualText, Comments, IsPrivate, TemplateID, Fields) VALUES(?,?,?,?,?,?,?)"
        self.database.execute( new_item, (str(name), "", "", "", str(isprivate), str(templateID), fields,) )
        self.database.create_collation("RMNOCASE", None)
        self.database.commit()
    def set_citation(self, sourceid, isprivate = 0, details = ""):
        '''
        Introduces a citation linked to the profile
        '''
        data_details = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?><Root><Fields><Field><Name>ItemID</Name><Value/></Field><Field>"
                        "<Name>Date</Name><Value/></Field><Field><Name>Details</Name><Value>")
        data_details += details
        data_details += "</Value></Field><Field><Name>Annotation</Name><Value/></Field></Fields></Root>"
        new_citation = ("INSERT INTO CitationTable(OwnerType, SourceID, OwnerID, Quality, IsPrivate,"
                        " Comments, ActualText, RefNumber,Flags, Fields) VALUES(0,?,?,?,?,?,?,?,0,?)")
        self.database.execute( new_citation, (str(sourceid), str(self.get_id()), "~~~", str(isprivate), details, "", "", data_details, ) )
        self.database.commit()
    def set_place_and_get_id(self,event):
        '''
        It will obtain or create a place id inside RootsMagic
        event is an instance of pyGenealogi.common_event, if not location is available will be ignored
        '''
        location = event.get_location()
        place_id = None
        if location:
            name_loc = location.get("formatted_location", location.get("raw"))
            place_id = self.get_place_id_by_name(name_loc)
            if not place_id:
                empty_value =""
                latitude = str(int(location.get("latitude", "0")*10000000))
                longitude = str(int(location.get("longitude", "0")*10000000))
                new_item = "INSERT INTO PlaceTable(PlaceType,Name,Abbrev,Normalized,Latitude,Longitude,LatLongExact,MasterID,Note) VALUES(1,?,?,?,?,?,0,0,?)"
                cursor = self.database.cursor()
                cursor.execute( new_item, (name_loc,empty_value,empty_value,latitude,longitude,empty_value,) )
                place_id = cursor.lastrowid
                self.database.commit()
        return place_id
    def setNewEvent(self,event):
        '''
        Overwrites the event from common profile adding the event
        event shall be of pyGenealogy common_event type
        '''
        place_id = self.set_place_and_get_id(event)
        if not place_id: place_id = "0"
        dateRTM = return_date_from_event(event)
        if not dateRTM: dateRTM = "."
        edit_date_value = str( (datetime.today()- datetime(1899,12,31) ).days +0.0)
        empty_value =""
        if event.get_event_type() in PERSONAL_EVENTS:
            new_event = ("INSERT INTO EventTable(EventType, OwnerType, OwnerID,FamilyID,PlaceID,SiteID,Date,IsPrimary,"
                         "IsPrivate,Proof,Status,EditDate,Sentence,Details,Note) VALUES(?,0,?,0,?,0,?,0,0,0,0,?,?,?,?)")
            self.database.execute( new_event, (DATE_EVENT_ID[event.get_event_type()],
                                str(self.get_id()),place_id,dateRTM,edit_date_value, empty_value,empty_value,empty_value, ) )
            self.database.commit()
    def setNewMarriage(self,event, family_id):
        '''
        Overwrites the event from common profile adding the event
        event shall be of pyGenealogy common_event type and a marriage event
        '''
        place_id = self.set_place_and_get_id(event)
        if not place_id: place_id = "0"
        dateRTM = return_date_from_event(event)
        if not dateRTM: dateRTM = "."
        edit_date_value = str( (datetime.today()- datetime(1899,12,31) ).days +0.0)
        empty_value =""
        if event.get_event_type() == "marriage":
            new_event = ("INSERT INTO EventTable(EventType, OwnerType, OwnerID,FamilyID,PlaceID,SiteID,Date,IsPrimary,"
                "IsPrivate,Proof,Status,EditDate,Sentence,Details,Note) VALUES(?,1,?,0,?,0,?,0,0,0,0,?,?,?,?)")
            self.database.execute( new_event, (DATE_EVENT_ID[event.get_event_type()],
                    str(family_id),place_id,dateRTM,edit_date_value, empty_value,empty_value,empty_value, ) )
            self.database.commit()
#===============================================================================
#         DELETE methods: methods to delete currently existing entries
#===============================================================================
    def del_web_ref(self, url):
        '''
        This function will delete the existing web reference, using the
        url as entry point (assumed to be unique)
        '''
        web_del = "DELETE FROM URLTable WHERE URL=? AND OwnerID=?"
        self.database.execute( web_del, ( url , str(self.get_id()),  ) )
        self.database.commit()
#===============================================================================
#         UPDATE methods: modified inputs which depend on database
#===============================================================================
    def update_web_ref(self, url = None, name = None, notes = None):
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
        elif name in self.get_all_url_names():
            if url:
                update_name = "UPDATE URLTable SET URL = ? WHERE Name=? AND OwnerID=?"
                self.database.execute( update_name, (str(url), str(name), str(self.get_id()), ) )
            if notes :
                update_note = "UPDATE URLTable SET Note = ? WHERE Name=? AND OwnerID=?"
                self.database.execute( update_note, (str(notes), str(name), str(self.get_id()), ) )
            self.database.commit()
            return True
        else:
            return None
    def update_research_item(self, log_id, repository , source = None, result = None):
        '''
        This function will update a given web reference
        '''
        if source :
            update_name = "UPDATE ResearchItemTable SET Source = ? WHERE Repository=? AND LogID=?"
            self.database.execute( update_name, (str(source), str(repository), str(log_id), ) )
        if result :
            update_note = "UPDATE ResearchItemTable SET Result = ? WHERE Repository=? AND LogID=?"
            self.database.execute( update_note, (str(result), str(repository), str(log_id), ) )
        self.database.commit()
        return True
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
    def return_person_data_in_NameTable(self, primary = 1):
        '''
        Common function used to get the table with the NameTable, used for name and surname
        '''
        input_person = "SELECT * FROM NameTable WHERE OwnerID=?"
        name_info = self.database.execute( input_person, (str(self.get_id()),) )
        loop_database = True
        array_nicks = []
        while loop_database:
            name_data = name_info.fetchone()
            if (name_data is not None):
                if (int(name_data[10]) == 1) and (primary == 1):
                    return name_data[3],name_data[2]
                elif (int(name_data[10]) == 0) and (primary == 0):
                    array_nicks.append(str(name_data[3]) + " " + str(name_data[2]))
            else:
                return array_nicks
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
            elif event_in_database[7][12] == "A":
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
            #We extract the geolocated string from the profile
            geo_string = place_info[2]
            #If was extracted before, we should avoid another geolocation call
            if get_geolocated_before(geo_string):
                event_output.setLocationAlreadyProcessed(get_geolocated_before(geo_string))
            else:
                event_output.setLocation(place_info[2])
                #We store the geolocation in the database for future use
                set_geolocated(geo_string, event_output.get_location())
            if int(place_info[5]) != 0 and int(place_info[6]) != 0:
                event_output.set_geo_location(int(place_info[5])/10000000, int(place_info[6])/10000000)
        return event_output