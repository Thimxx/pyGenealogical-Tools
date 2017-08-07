# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

import requests

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni.geni_settings as s




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
                #Good... now we iterate per union the profiles found!
                #Now, let's create tmp variables for capturing the union information
                tmp_parents = []
                tmp_child = []
                myidischild = False
                
                for tmp_profile in data["nodes"][keydata]["edges"]:
                    
                    # When we detect the current profile we skip it!!!
                    if (tmp_profile == myid):
                        #but before exiting we check if is the relatinohip of fathers!!!
                        if (data["nodes"][keydata]["edges"][tmp_profile]['rel'] == "child"):
                            myidischild = True
                    else:
                        if (data["nodes"][keydata]["edges"][tmp_profile]['rel'] == "child"):
                            tmp_child.append(tmp_profile)
                        else:
                            tmp_parents.append(tmp_profile)
                #Great, now we do the append
                if myidischild:
                    #If this is a child, parents of the relationship are her parents and children the sibligns
                    parents = parents + tmp_parents
                    #Reminder!!! Here we do not see the half-brothers!
                    sibligns = sibligns + tmp_child
                else:
                    #In this case this union reflects her actual children!!!                    
                    partner = partner + tmp_parents
                    children = children + tmp_child
                
        self.parents = parents
        self.sibligns = sibligns
        self.partner = partner
        self.children = children
        return None

#===================================================
# Util functions
#===================================================

def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))
