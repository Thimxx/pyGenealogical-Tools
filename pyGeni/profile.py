# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

import requests

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni.geni_settings as s
from pyGeni.data_models import geni_union




class profile:
    def __init__(self, id_geni, token, type_geni="g"):  # id int or string
        self.token = token
        # Validate access token, connecting to Geni, this might take a while
        valid_token = requests.get(s.GENI_VALIDATE_TOKEN + self.token).json()

        self.tokenIsOk = False
        if ( str(valid_token['result']) == "OK"):
            self.tokenIsOk = True
            
        url = s.GENI_PROFILE + type_geni + str(id_geni) + self.token_string()
        r = requests.get(url)
        data = r.json()

        if type == "g":
            self.guid = id_geni
            self.id = stripId(data["id"])
        if type == "":
            self.id = id_geni
            self.guid = int(data["guid"])

        self.fulldata = data
        if "mugshot_urls" in data:
            data.pop("mugshot_urls")
        if "photo_urls" in data:
            data.pop("photo_urls")
        self.data = data

        self.unions_parsed = False
        self.parents = []
        self.sibligns = []
        self.partner = []
        self.children = []
        
        self.get_relations()


    def nameLifespan(self):
        birth = self.data.get("birth", {}).get("date", {}).get("year", "?")
        death = self.data.get("death", {}).get("date", {}).get("year", "?")
        if birth == "?" and death == "?":
            return self.data["name"]
        else:
            return self.data["name"] + " (" + str(birth) + " - " + str(death) + ")"


    def token_string(self):
        return s.GENI_TOKEN + self.token
    
    def get_relations(self):
        '''
        Get relations by using the immediate family api
        '''
        #we initialize the lists
        parents = []
        sibligns = []
        partner = []
        children = []
        url = self.data["url"] + s.GENI_FAMILY + self.token_string()
        r = requests.get(url)
        data = r.json()
        
        myid = self.data["id"]
        #the nodes include the data of the different affected profiles and unions
        for keydata in data["nodes"].keys():
            #is easier to go to the usions, so we filter by unions.
            if "union" in keydata:
                #Good... let's obtain the data from the union
                tmp_union = geni_union(data["nodes"][keydata], keydata)
                
                #Now we need to filter the parents and children as we should not duplicate
                if tmp_union.is_profile_child(myid):
                    #We know is a child... so
                    parents = parents + tmp_union.parents
                    tmp_union.children.remove(myid)
                    sibligns = sibligns + tmp_union.children
                else:
                    tmp_union.parents.remove(myid)
                    partner = partner +  tmp_union.parents
                    children = children + tmp_union.children
                  
        self.parents = parents
        self.sibligns = sibligns
        self.partner = partner
        self.children = children
        return None
    
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
