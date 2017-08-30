# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni as s
from pyGeni.geniapi_common import geni_calls
from pyGeni.immediate_family import immediate_family


class profile(geni_calls):
    def __init__(self, id_geni, token, type_geni="g"):  # id int or string
        self.properly_executed = False
        #We initiate the base class
        geni_calls.__init__(self, token)
        url = s.GENI_PROFILE + type_geni + str(id_geni) + self.token_string()
        r = s.geni_request_get(url)
        data = r.json()
        if not "error" in data.keys():
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


    def nameLifespan(self):
        birth = self.data.get("birth", {}).get("date", {}).get("year", "?")
        death = self.data.get("death", {}).get("date", {}).get("year", "?")
        if birth == "?" and death == "?":
            return self.data["name"]
        else:
            return self.data["name"] + " (" + str(birth) + " - " + str(death) + ")"


    
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

#===================================================
# Util functions
#===================================================

def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))
