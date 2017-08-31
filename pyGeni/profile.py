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
from datetime import date


class profile(geni_calls, gen_profile):
    def __init__(self, id_geni, token, type_geni="g"):  # id int or string
        #Some checking parameters initiated
        self.properly_executed = False
        self.existing_in_geni = False
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
            if type_geni == "g":
                self.guid = id_geni
                self.id = stripId(data["id"])
            if type_geni == "":
                self.id = id_geni
                self.guid = int(data["guid"])

            self.fulldata = data
            if "mugshot_urls" in data:
                data.pop("mugshot_urls")
            if "photo_urls" in data:
                data.pop("photo_urls")
            self.data = data
            self.get_relations()
            self.properly_executed = True
   
    def get_relations(self):
        '''
        Get relations by using the immediate family api
        '''
        
        self.relations = immediate_family(self.token, self.data["id"])
        
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
        
        

#===================================================
# Util functions
#===================================================

def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))
