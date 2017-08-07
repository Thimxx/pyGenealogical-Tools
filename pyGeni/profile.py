# Several ideas for this file were taken from: https://github.com/liuyao12/GeniBot/blob/master/geni_api.py
# Actually, the initial version is a reordering of that version.
# All credits to the original creator of that file: liuyao12

import requests

#If importing this module is providing an error, check the installation instructions, you need to create a local
#copy of geni_settings_template
import pyGeni.geni_settings as s


# Validate access token, connecting to Geni, this might take a while
valid_token = requests.get(s.GENI_VALIDATE_TOKEN + s.TOKEN).json()


tokenIsOk = False
if ( str(valid_token['result']) == "OK"):
    tokenIsOk = True

class profile:
    def __init__(self, id_geni, type_geni="g"):  # id int or string
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


    def nameLifespan(self):
        birth = self.data.get("birth", {}).get("date", {}).get("year", "?")
        death = self.data.get("death", {}).get("date", {}).get("year", "?")
        if birth == "?" and death == "?":
            return self.data["name"]
        else:
            return self.data["name"] + " (" + str(birth) + " - " + str(death) + ")"


    def relations(self):
        '''
        This function will drive a map of all relationships inside the profile
        :return:
        '''
        parents = []
        sibligns = []
        partner = []
        children = []
        unions = self.data.get("unions")
        for union in unions:

            tmp_spouses, tmp_children, parent_marriage = self.parse_union(union)
            if parent_marriage:
                #Ok, this is the marriage of the parents
                parents = parents + tmp_spouses
                sibligns = sibligns + tmp_children
            else:
                #In this case we are talking about the marraige... it could be several
                partner = partner + tmp_spouses
                children = children + tmp_children

        self.unions_parsed = True
        self.parents = parents
        self.sibligns = sibligns
        self.partner = partner
        self.children = children
        return None



    def parse_union(self, union):
        '''
        This function obtains the people involved in each of the unions.
        :param union: obtained in the format of link without the token data
        :return: spouses: will be the spouses without the involved profile
                children: all childrens of the involved profile
                parent_marriage: will be True if the union refers to the marriage of the parents.
        '''
        parent_marriage = False
        spouses = []
        children = []
        url = union + self.token_string()
        r = requests.get(url).json()
        for url in r.get("partners"):
            idg = stripId(url)
            temp_parent = profile(idg, "")
            if not (self.data["url"] == url):
                spouses.append(temp_parent)

        for url in r.get("children"):
            idg = stripId(url)
            temp_parent = profile(idg, "")
            if not (self.data["url"] == url):
                children.append(temp_parent)
            else:
                parent_marriage = True
        return spouses, children, parent_marriage

    def token_string(self):
        return s.GENI_TOKEN + s.TOKEN

#===================================================
# Util functions
#===================================================

def stripId(url):  # get node id from url (not guid)
    return (int(url[url.find("profile-") + 8:]))
