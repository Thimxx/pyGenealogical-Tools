# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni as s
from pyGeni.geniapi_common import geni_calls
from pyGeni.immediate_family import immediate_family
from pyGenealogy.common_profile import gen_profile
from pyGenealogy import NOT_KNOWN_VALUE
from messages.pygeni_messages import ABOUT_ME_MESSAGE
from datetime import date

SPECIFIC_GENI_STRING = ['id', 'url', 'profile_url', 'creator' ]
SPECIFIC_GENI_BOOLEAN =  ['public', 'is_alive', 'deleted']
SPECIFIC_GENI_INTEGER = ['guid', 'created_at', 'updated_at']
#TODO: review teh complete post method and include all fields here : https://www.geni.com/platform/developer/help/api?path=profile%2Fadd-child&version=1
DATA_STRING_IN_GENI = { "name" : "first_name", "surname" : "last_name",  
                       "gender": "gender", "comment": "about_me"}
#TODO: think about a logic for display name...
NOT_USED = {"name_to_show" : "display_name"}
EQUIVALENT_SEX = { "male" : "M", "female" : "F"}

GENI_EVENT_DATA = {"birth" : {"date":"birth_date", "accuracy": "accuracy_birth_date", "location": "birth_place" },
                   "death" : {"date":"death_date", "accuracy": "accuracy_death_date", "location": "death_place" },
                   "baptism" : {"date":"baptism_date", "accuracy": "accuracy_baptism_date", "location": "baptism_place" },
                   "burial" : {"date":"burial_date", "accuracy": "accuracy_burial_date", "location": "burial_place"}
                   }

class profile(geni_calls, gen_profile):
    def __init__(self, id_geni, token, type_geni="g"):  # id int or string
        #Some checking parameters initiated
        self.properly_executed = False
        self.existing_in_geni = False
        self.geni_specific_data = {}
        #We initiate the base classes
        geni_calls.__init__(self, token)
        url = s.GENI_PROFILE + type_geni + str(id_geni) + self.token_string()
        r = s.geni_request_get(url)
        data = r.json()
        #Now we can execute the constructor
        if (not "first_name" in data.keys()): data["first_name"] = NOT_KNOWN_VALUE
        if (not "last_name" in data.keys()): data["last_name"] = NOT_KNOWN_VALUE
        gen_profile.__init__(self, data["first_name"], data["last_name"], )
        self.transfer_to_base(data)
        if not "error" in data.keys():
            self.existing_in_geni = True
            self.fulldata = data
            if "mugshot_urls" in data:
                data.pop("mugshot_urls")
            if "photo_urls" in data:
                data.pop("photo_urls")
            self.data = data
            self.get_geni_data(data)
            self.properly_executed = True
   
    def get_relations(self):
        '''
        Get relations by using the immediate family api
        '''
        
        self.relations = immediate_family(self.token, self.geni_specific_data['id'])
        
        self.parents = self.relations.parents
        self.sibligns = self.relations.sibligns
        self.partner = self.relations.partner
        self.children = self.relations.children
        
    
    def get_id(self):
        '''
        Simple function to get Geni ID
        '''
        return self.data['id']
    def transfer_to_base(self, data):
        '''
        This function translates to the base class the data extracted from geni
        '''
        #TODO: we need a complete review of this profile, on demand to be created
        data.get("birth", {}).get("date", {}).get("year", "?")
        if (data.get("birth", {}).get("date", {}) != {}): 
            format_date, accuracy_geni = self.get_date(data.get("birth", {}).get("date", {}))
            self.setCheckedBirthDate(format_date, accuracy=accuracy_geni)
        if (data.get("death", {}).get("date", {}) != {}):  
            format_date, accuracy_geni = self.get_date(data.get("death", {}).get("date", {}))
            self.setCheckedDeathDate(format_date, accuracy=accuracy_geni)
        #TODO: introduce further parameters
         
    def get_date(self, data_dict):
        '''
        Get date from the Geni standard
        '''
        #TODO: this needs a restructuring when changing as well the data model of dates.
        accuracy = None
        date_received = None
        if (data_dict.get("year",None) != None): date_received = date(data_dict.get("year"), data_dict.get("month", 1), data_dict.get("day", 1))
        if (data_dict.get("circa", "false") == "true"): accuracy = "ABOUT"
        elif (data_dict.get("range", "before") == "true"): accuracy = "BEFORE"
        elif (data_dict.get("range", "after") == "true"): accuracy = "AFTER"
        else: accuracy = "EXACT"
        return date_received, accuracy
    def get_geni_data(self, data):
        '''
        Transfer json geni data into the base profile
        '''
        #We just add one by one all the different values specific to Geni
        for value in SPECIFIC_GENI_STRING:
            self.geni_specific_data[value] = data[value]
        for value in SPECIFIC_GENI_BOOLEAN:
            self.geni_specific_data[value] = bool(data[value])
        for value in SPECIFIC_GENI_INTEGER:
            self.geni_specific_data[value] = int(data[value])
        self.get_relations()
        #These are the general profiles values
        for value_geni in data.keys():
            #We check if belongs to the values we have matched
            if value_geni in DATA_STRING_IN_GENI.values():
                #Great, now we need to know the equivalent value inside the common_profile value
                data_location = list(DATA_STRING_IN_GENI.values()).index(value_geni)
                value_profile = list(DATA_STRING_IN_GENI.keys())[data_location]
                if (value_profile == "gender"):
                    self.setCheckedGender(EQUIVALENT_SEX[data[value_geni]])
                else:
                    self.gen_data[value_profile] = data[value_geni]
                
    @classmethod
    def create_as_a_child(cls, base_profile, token, union):
        '''
        From a common profile from pyGenealogy library, a new profile will be created
        as a child of a given union of 2 profiles.
        '''
        #Calling essentially the constructors
        base_profile.__class__ = cls
        geni_calls.__init__(cls, token)
        #Some checking parameters initiated
        base_profile.properly_executed = False
        base_profile.existing_in_geni = False
        base_profile.data = {}
        base_profile.geni_specific_data = {}
        #We create the url for creating the child
        add_child = s.GENI_API + union + s.GENI_ADD_CHILD + s.GENI_INITIATE_PARAMETER + "first_name="
        add_child += base_profile.gen_data["name"] + s.GENI_ADD_PARAMETER + s.GENI_TOKEN + cls.token
        #We also add the needed data, that we take from the base profile directly
        data_input = base_profile.create_input_file_2_geni()
        r = s.geni_request_post(add_child, data_input=data_input)
        data = r.json()
        if not "error" in data.keys():
            base_profile.data = data
            base_profile.properly_executed = True
            base_profile.existing_in_geni = True
            base_profile.id = stripId(data["id"])
            base_profile.guid = int(data["guid"])
            base_profile.get_geni_data(data)
        
    def delete_profile(self):
        '''
        We delete this profile from Geni
        '''
        url_delete = s.GENI_PROFILE + self.geni_specific_data['id'] + s.GENI_DELETE + self.token_string()
        r = s.geni_request_post(url_delete)
        self.data = r.json()
        if ( self.data.get("result", None) == "Deleted"):
            self.existing_in_geni = False
            #Essentially, we delete all GENI data
            self.geni_specific_data = {}
            return True
        else:
            return False
    
    def create_input_file_2_geni(self):
        '''
        This method will return the Json file that will be used as input
        for the post file
        '''
        data = {}
        for profile_value in DATA_STRING_IN_GENI.keys():
            if (self.gen_data.get(profile_value, None) != None):
                data[DATA_STRING_IN_GENI[profile_value]] = self.gen_data[profile_value]
        if [self.gen_data["web_ref"] != []]:
            msg = ABOUT_ME_MESSAGE
            for value in self.gen_data["web_ref"]:
                msg += " [" + value + " FamilySearch-link]"
            data["about_me"] = msg
        for event_geni in GENI_EVENT_DATA:
            date = self.gen_data.get(GENI_EVENT_DATA[event_geni]["date"], None)
            accuracy = self.gen_data.get(GENI_EVENT_DATA[event_geni]["accuracy"], None)
            location = self.gen_data.get(GENI_EVENT_DATA[event_geni]["location"], None)
            event_value = getEventStructureGeni(date, accuracy, location)
            if (event_value): data[event_geni] = event_value
        return data
        

#===================================================
# Util functions
#===================================================

def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))

def getDateStructureGeni(date, accuracy):
    '''
    Generates a Data structure to be introduced in Geni input
    '''
    data_values = {}
    if (date != None):
        if accuracy == "ABOUT":
            data_values['circa'] = True
            data_values['year'] = date.year
        else:
            if accuracy == "BEFORE":
                data_values['range'] = "before"
            elif accuracy == "AFTER":
                data_values['range'] = "after"
            data_values['year'] = date.year
            data_values['month'] = date.month
            data_values['day'] = date.day
    return data_values

def getLocationStructureGeni(location):
    '''
    Converts the location in common profile into a structure readable by
    geni
    '''
    location_data = {}
    if(location != None):
        for key in location.keys():
            if (key != "raw"):
                location_data[key] = location[key]
    return location_data

def getEventStructureGeni(date, accuracy, location):
    '''
    Creates an event structure for geni
    '''
    event_data = {}
    date_structure = getDateStructureGeni(date, accuracy)
    location_structure = getLocationStructureGeni(location)
    if(date_structure) : event_data["date"] = date_structure
    if(location_structure) :event_data["location"] = location_structure
    return event_data
    
        
        
    
