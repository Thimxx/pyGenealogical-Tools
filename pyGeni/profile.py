# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni as s
from pyGeni.geniapi_common import geni_calls
from pyGeni.immediate_family import immediate_family
from pyGenealogy.common_profile import gen_profile, EVENT_DATA, EVENT_TYPE
from pyGenealogy import NOT_KNOWN_VALUE
from messages.pygeni_messages import ABOUT_ME_MESSAGE, ERROR_REQUESTS, RESIDENCE_MESSAGE, NO_VALID_UNION_PROFILE
import logging

SPECIFIC_GENI_STRING = ['id', 'url', 'profile_url', 'creator' ]
SPECIFIC_GENI_BOOLEAN =  ['public', 'is_alive', 'deleted']
SPECIFIC_GENI_INTEGER = ['guid', 'created_at', 'updated_at']
#TODO: review teh complete post method and include all fields here : https://www.geni.com/platform/developer/help/api?path=profile%2Fadd-child&version=1
DATA_STRING_IN_GENI = { "name" : "first_name", "surname" : "last_name",
                       "gender": "gender", "comment": "about_me"}
DATA_LIST_IN_GENI = {"nicknames": "nicknames"}
#TODO: think about a logic for display name...
NOT_USED = {"name_to_show" : "display_name"}
EQUIVALENT_SEX = { "male" : "M", "female" : "F"}



class profile(geni_calls, gen_profile):
    def __init__(self, geni_input, type_geni="g"):  # id int or string
        '''
        The geni input provided can be:
        - The id of the profile
        - The id of the profile with g
        - Each address of the profile.
        '''
        #Some checking parameters initiated
        self.properly_executed = False
        self.existing_in_geni = False
        self.geni_specific_data = {}
        #We initiate the base classes
        geni_calls.__init__(self)
        url = process_geni_input(geni_input, type_geni) + self.token_string()
        r = s.geni_request_get(url)
        data = r.json()
        #Now we can execute the constructor
        if (not "first_name" in data.keys()): data["first_name"] = NOT_KNOWN_VALUE
        if (not "last_name" in data.keys()): data["last_name"] = NOT_KNOWN_VALUE
        gen_profile.__init__(self, data["first_name"], data["last_name"], )
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
        self.relations = immediate_family(self.geni_specific_data['id'])
        self.parents = self.relations.parents
        self.sibligns = self.relations.sibligns
        self.partner = self.relations.partner
        self.children = self.relations.children
        self.parent_union = self.relations.parent_union
        self.marriage_union = self.relations.marriage_union
        #TODO:This is temporal, only a single marriage is considered
        if (len(self.relations.marriage_events) > 0):
            self.setNewEvent(self.relations.marriage_events[0])
    def get_id(self):
        '''
        Simple function to get Geni ID
        '''
        return self.data['id']
    def get_geni_data(self, data):
        '''
        Transfer json geni data into the base profile
        '''
        #We just add one by one all the different values specific to Geni
        for value in SPECIFIC_GENI_STRING:
            if value in data.keys() : self.geni_specific_data[value] = data[value]
        for value in SPECIFIC_GENI_BOOLEAN:
            if value in data.keys() : self.geni_specific_data[value] = bool(data[value])
        for value in SPECIFIC_GENI_INTEGER:
            if value in data.keys() : self.geni_specific_data[value] = int(data[value])
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
            elif value_geni in DATA_LIST_IN_GENI.values():
                data_location = list(DATA_LIST_IN_GENI.values()).index(value_geni)
                value_profile = list(DATA_LIST_IN_GENI.keys())[data_location]
                self.gen_data[value_geni] = data[value_geni]
            elif value_geni in EVENT_TYPE:
                current_event = self.get_date(value_geni, data.get(value_geni, {}).get("date", {}))
                current_event.setLocationAlreadyProcessed(data.get(value_geni, {}).get("location", {}))
                self.gen_data[value_geni] = current_event
    def add_marriage_in_geni(self, union = None):
        '''
        This method add marriage data in geni, add union if there is no unique
        marriage
        '''
        if (union == None):
            #If no union is added is because is the unique...
            if(len(self.marriage_union) == 1):
                union = self.marriage_union[0].union_id
            else:
                #If we have more than one marriage we cannot proceed
                return False
        #We create the url for creating the child
        update_marriage = s.GENI_API + union + s.GENI_UPDATE + s.GENI_INITIATE_PARAMETER +  s.GENI_TOKEN + s.get_token()
        #We add the event data for marriage
        data_input={}
        event_value = self.event_value( "marriage")
        if (event_value): data_input["marriage"] = event_value
        #We also add the needed data, that we take from the base profile directly
        r = s.geni_request_post(update_marriage, data_input=data_input)
        data = r.json()
        if "error" in data.keys():
            logging.error(ERROR_REQUESTS + data["error"])
            #TODO: process the data creation and update relations
    @classmethod
    def create_internally(cls, geni_input , type_geni):
        return cls(geni_input , type_geni)
    def creation_operations(self, adding_input):
        '''
        Common functions on creating profiles
        '''
        #Some checking parameters initiated
        self.properly_executed = False
        self.existing_in_geni = False
        self.data = {}
        self.geni_specific_data = {}
        #We also add the needed data, that we take from the base profile directly
        data_input = self.create_input_file_2_geni()
        r = s.geni_request_post(adding_input, data_input=data_input)
        data = r.json()
        if not "error" in data.keys():
            self.data = data
            self.properly_executed = True
            self.existing_in_geni = True
            self.id = stripId(data["id"])
            self.guid = int(data["guid"])
            self.get_geni_data(data)
    @classmethod
    def create_as_a_child(cls, base_profile, union = None, profile = None,
                          geni_input = None, type_geni="g"):
        '''
        From a common profile from pyGenealogy library, a new profile will be created
        as a child of a given union of 2 profiles.
        '''
        union_to_use = None
        if (union != None):
            union_to_use = union
        elif (profile != None):
            if (len(profile.marriage_union) == 1):
                union_to_use = profile.marriage_union[0].union_id
        elif (geni_input != None):
            tmp_prof = cls.create_internally(geni_input, type_geni)
            #TODO: add error checking if tmp_prof is not properly created.
            if (len(tmp_prof.marriage_union) == 1):
                union_to_use = tmp_prof.marriage_union[0].union_id
            else:
                #We have a problem, potentially a wrong profile
                logging.error(NO_VALID_UNION_PROFILE + str(len(tmp_prof.marriage_union)))
        if (union_to_use == None): return False
        #Calling essentially the constructors
        base_profile.__class__ = cls
        geni_calls.__init__(cls)
        #We create the url for creating the child
        add_child = s.GENI_API + union_to_use + s.GENI_ADD_CHILD + s.GENI_INITIATE_PARAMETER + "first_name="
        add_child += base_profile.gen_data["name"] + s.GENI_ADD_PARAMETER + s.GENI_TOKEN + s.get_token()
        base_profile.creation_operations(add_child)
        return True
    @classmethod
    def create_as_a_parent(cls, base_profile, profile = None,
                          geni_input = None, type_geni="g"):
        '''
        From a common profile from pyGenealogy library, a new profile will be created
        as a parent of a given profile
        '''
        child_to_use = process_profile_input(profile, geni_input, type_geni)
        #Calling essentially the constructors
        base_profile.__class__ = cls
        geni_calls.__init__(cls)
        #We create the url for creating the child
        add_parent = child_to_use + s.GENI_ADD_PARENT + s.GENI_INITIATE_PARAMETER  + s.GENI_TOKEN + s.get_token()
        #We also add the needed data, that we take from the base profile directly
        base_profile.creation_operations(add_parent)
    @classmethod
    def create_as_a_partner(cls, base_profile, profile = None,
                          geni_input = None, type_geni="g"):
        '''
        From a common profile we take another profile and we create at parnter.
        '''
        partner_to_use = process_profile_input(profile, geni_input, type_geni)
        #Calling essentially the constructors
        base_profile.__class__ = cls
        geni_calls.__init__(cls)
        #We create the url for creating the child
        add_partner = partner_to_use + s.GENI_ADD_PARTNER + s.GENI_INITIATE_PARAMETER + "first_name="
        add_partner += base_profile.gen_data["name"] + s.GENI_ADD_PARAMETER + s.GENI_TOKEN + s.get_token()
        base_profile.creation_operations(add_partner)
        base_profile.add_marriage_in_geni()
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
        data["public"] = "false"
        for profile_value in DATA_STRING_IN_GENI.keys():
            if (self.gen_data.get(profile_value, None) != None):
                data[DATA_STRING_IN_GENI[profile_value]] = self.gen_data[profile_value]
        for list_data in DATA_LIST_IN_GENI:
            if (self.gen_data.get(list_data, None) != None):
                #Needs to be converted in a comman separated list
                data[DATA_LIST_IN_GENI[list_data]] = ",".join(self.gen_data[list_data])
        if [self.gen_data["web_ref"] != []]:
            msg = ABOUT_ME_MESSAGE
            for value in self.gen_data["web_ref"]:
                msg += " [" + value + " FamilySearch-link]"
            data["about_me"] = msg
        for event_geni in EVENT_DATA:
            event_value = self.event_value(event_geni)
            if (event_value): data[event_geni] = event_value
        event_residence = self.event_value("residence")
        if (event_residence):
            msg = RESIDENCE_MESSAGE
            if event_residence.get("date", {}).get("year", None):
                msg += " Year = " + str(event_residence.get("date", {}).get("year", None))
            if event_residence.get("date", {}).get("month", None):
                msg += " Month = " + str(event_residence.get("date", {}).get("month", None))
            if event_residence.get("date", {}).get("day", None):
                msg += " Day = " + str(event_residence.get("date", {}).get("day", None))
            if self.gen_data.get("residence_place", {}).get("raw", None):
                msg += " Location = " + self.gen_data.get("residence_place", {}).get("raw", None)
            data["about_me"] += msg
        return data
    def event_value(self, event_geni):
        '''
        Provides event value, uses the function
        '''
        event_data = {}
        if event_geni in self.gen_data.keys():
            date_structure = getDateStructureGeni(self.gen_data[event_geni])
            location_structure = getLocationStructureGeni(self.gen_data[event_geni].get_location())
            if(date_structure) : event_data["date"] = date_structure
            if(location_structure) :event_data["location"] = location_structure
        return event_data
#===================================================
# Util functions
#===================================================
def process_geni_input(geni_input, type_geni):
    '''
    This input provides needed input for accessing the profile
    '''
    if ("/api" in str(geni_input)):
        return geni_input
    elif ("profile" in str(geni_input)):
        return s.GENI_API + str(geni_input)
    elif ("/people/" in str(geni_input)):
        #The ?through is in case the use has introduced the complete address
        return s.GENI_PROFILE + "g" + geni_input.split("?through")[0].split("/")[-1]
    else:
        return s.GENI_PROFILE + type_geni + str(geni_input)
def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))
def getDateStructureGeni(event):
    '''
    Generates a Data structure to be introduced in Geni input
    '''
    accuracy = event.get_accuracy()
    data_values = {}
    if (event.get_year() or event.get_month() or event.get_day()):
        if (event.get_year()) : data_values['year'] = event.get_year()
        if (event.get_month()) : data_values['month'] = event.get_month()
        if (event.get_day()) : data_values['day'] = event.get_day()
        if accuracy == "ABOUT":
            data_values['circa'] = True
        else:
            if accuracy == "BEFORE":
                data_values['range'] = "before"
            elif accuracy == "AFTER":
                data_values['range'] = "after"
            elif accuracy == "BETWEEN":
                data_values['range'] = "between"
                if (event.get_year_end()) : data_values['end_year'] = event.get_year_end()
                if (event.get_month_end()) : data_values['end_month'] = event.get_month_end()
                if (event.get_day_end()) : data_values['end_day'] = event.get_day_end()
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
def process_profile_input(profile = None, geni_input = None, type_geni="g"):
    '''
       Function to avoid code duplication that takes returns the right profile id
    '''
    profile_to_use = None
    if (profile != None):
        profile_to_use = profile.geni_specific_data["url"]
    elif (geni_input != None):
        profile_to_use = process_geni_input(geni_input, type_geni)
    return profile_to_use