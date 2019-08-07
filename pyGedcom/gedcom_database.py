'''
Created on 28 jul. 2019

@author: Val
'''
from pyGenealogy.common_database import gen_database, CHAR_FAM, CHAR_PROF
from pyGedcom.gedcom_family import family_gedcom
from pyGedcom.gedcom_profile import gedcom_profile
#These are the tags that should contain a family
listing_tags = ["CHIL"]

class db_gedcom(gen_database):
    '''
    This is wrapper for reading the database of GEDCOM file.
    '''
    def __init__(self, gedcomfile = None):
        '''
        Constructor of the database introducing as input the database
        '''
        gen_database.__init__(self)
        if gedcomfile:
            f = open(gedcomfile, "r")
            self.gedcom = recursive_analysis(f, 0)
            f.close()
        else:
            #In this case there is not database, so requires creation
            self.gedcom = {}
            self.gedcom["HEAD"] = {'SOUR': {'NAME': {'VALUE': 'Created using https://github.com/Thimxx/pyGenealogical-Tools'}}}
            self.gedcom["GEDC"] = {'VERS': {'VALUE': '5.5'}}
            self.gedcom["TRLR"] = {}
        id_found = False
        count_prof = 0
        while not id_found:
            if "@" + CHAR_PROF + str(count_prof + 1) + "@" in self.gedcom.keys():
                count_prof += 1
            else:
                self.count_prof = count_prof
                id_found = True
        id_found = False
        count_fam = 0
        while not id_found:
            if "@" + CHAR_PROF + str(count_fam + 1) + "@" in self.gedcom.keys():
                count_fam += 1
            else:
                self.count_fam = count_fam
                id_found = True
        self.count_fam = 0
#===============================================================================
#         GET methods: to be used by all upper functions or be replace
#===============================================================================
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        return gedcom_profile(self.gedcom[id_profile])
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        return family_gedcom(self.gedcom[id_family])
    def get_all_profiles(self):
        '''
        Returns all profiles in the database
        '''
        profiles = []
        for id_key in self.gedcom:
            if self.gedcom[id_key].get("VALUE", None) == "INDI":
                profiles.append(gedcom_profile(self.gedcom[id_key]))
        return profiles
    def save_gedcom_file(self, file):
        '''
        This function will save the gedcomfile to a new file that can support on exportation
        '''
        lines =database_2_gedcom(self.gedcom, 0)
        f = open(file, "w")
        for line in lines:
            f.write(line+"\n")
        f.close()
#===============================================================================
#         ADD methods: Add methods used to include a new profile and new family
#===============================================================================
    def add_profile(self, profile):
        '''
        It will add a new profile in the database
        '''
        self.count_prof += 1
        id_prof = "@" + CHAR_PROF + str(self.count_prof)+ "@"
        self.gedcom.pop("TRLR", None)
        self.gedcom[id_prof] = profile.individual
        self.gedcom["TRLR"] = {}
        #Finally we add the information to the profile
        profile.set_id(id_prof)
        return id_prof
    def add_family(self, father = None, mother = None, children = None, marriage = None):
        '''
        It will create and add a new family to the database
        it is better that each database will create their own families
        '''
        self.count_fam += 1
        id_fam = "@" + CHAR_FAM + str(self.count_fam)+ "@"
        fam = family_gedcom(father = father, mother = mother, child = children, marriage = marriage)
        self.gedcom.pop("TRLR", None)
        self.gedcom[id_fam] = fam.family
        self.gedcom["TRLR"] = {}
        return id_fam
#===============================================================================
#         Some particular functions of this modules
#===============================================================================
def recursive_analysis(listed_data, level):
    '''
    This function allows to perform a recursive analysis of the GEDCOM file
    '''
    output_dict = {}
    next_analysis = []
    first_read = True
    key = None
    value = None
    for line in listed_data:
        s_line = line.rstrip().split(" ", 2)
        if int(s_line[0]) == level:
            #If it is the second time, then the data shall be captured in the new one!
            if not first_read:
                next_dict = {}
                if len(next_analysis) > 0: next_dict = recursive_analysis(next_analysis, level + 1)
                #This might create infinite loop if not done!
                next_analysis = []
                #We introduce the value
                if value: next_dict["VALUE"] = value
                output_dict[key] =  next_dict
            else:
                first_read = False
            #We store the key and value for the next iteration.
            key = s_line[1]
            #Notice that we can have duplicated lines one followed by the next, and we shall ensure we capture all values
            if key in listing_tags:
                #In a proper gedcom, we cannot not have 2 listnig values followed
                if isinstance(value, list): value.append(s_line[2])
                else: value = [s_line[2]]
            elif len(s_line) == 3: value = s_line[2]
            else: value = None
        else:
            next_analysis.append(line)
    #The last entry in the value is not considered
    next_dict = {}
    if len(next_analysis) > 0: next_dict = recursive_analysis(next_analysis, level + 1)
    if value: next_dict["VALUE"] = value
    output_dict[key] =  next_dict
    return output_dict
def database_2_gedcom(ged_dict, level):
    '''
    This function will transform the current database dictionary into a gedcom writable format
    '''
    output = []
    for key in ged_dict:
        if key != "VALUE":
            #Notice that listing tags will contain a list of parameters, and shall be written in a different approach
            if not key in listing_tags:
                line = str(level) + " " + key + " " + ged_dict.get(key).get("VALUE", "")
                output.append(line)
            else:
                #We need to perform a loop here.
                for list_tag in ged_dict.get(key).get("VALUE", []):
                    line = str(level) + " " + key + " " + list_tag
                    output.append(line)
            #If there are lower lines we need to add them
            lower_lines = database_2_gedcom(ged_dict.get(key), level +1)
            output += lower_lines
    return output