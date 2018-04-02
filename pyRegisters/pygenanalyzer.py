'''
Created on 28 mar. 2018

@author: Val
'''

from pyGenealogy.common_profile import gen_profile
from pyRegisters.pyrememori import rememori_reader
from pyRegisters.pyelnortedecastilla import elnortedecastilla_reader
import datetime, logging

class gen_analyzer(object):
    '''
    This class will accept a given GEDCOM file for later on executing all pyRegister modules, final
    output will be a description of potential matches for helping in investigation.
    '''
    def __init__(self, gedcomfile, language = "en", name_convention= "father_surname"):
        '''
        Introduce a gedcomfile in GEDCOM format
        '''
        self.gedcomfile = gedcomfile
        self.language = language
        self.name_convention = name_convention
        self.profiles = []
        for ele in self.gedcomfile.__dict__["root_elements"]:
            if(ele.tag == "INDI"):
                profile = gen_profile("", "")
                for sub_ele in ele.__dict__['child_elements']:
                    if sub_ele.tag == "NAME":
                        for name_ele in sub_ele.__dict__['child_elements']:
                            if (name_ele.tag == "GIVN"): profile.set_name(name_ele.value)
                            if (name_ele.tag == "SURN"): profile.set_surname(name_ele.value)
                    if sub_ele.tag == "BAPM":
                        for name_ele in sub_ele.__dict__['child_elements']:
                            if (name_ele.tag == "DATE"):
                                profile.setCheckedDate("baptism_date", datetime.datetime.strptime(name_ele.value.replace("BEF ", "").replace("AFT ", "").replace("ABT ", ""), "%d %b %Y" ).date(), accuracy_data(name_ele.value))
                    if sub_ele.tag == "BIRT":
                        for name_ele in sub_ele.__dict__['child_elements']:
                            if (name_ele.tag == "DATE"):
                                profile.setCheckedDate("birth_date", datetime.datetime.strptime(name_ele.value.replace("BEF ", "").replace("AFT ", "").replace("ABT ", ""), "%d %b %Y" ).date(), accuracy_data(name_ele.value))
                    if sub_ele.tag == "DEAT":
                        for name_ele in sub_ele.__dict__['child_elements']:
                            if (name_ele.tag == "DATE"):
                                profile.setCheckedDate("death_date", datetime.datetime.strptime(name_ele.value.replace("BEF ", "").replace("AFT ", "").replace("ABT ", ""), "%d %b %Y" ).date(), accuracy_data(name_ele.value))
                         
                self.profiles.append(profile)
    def execute(self, output = None):
        '''
        This will execute all checkings of data with other sources.
        '''
        self.file = None
        if not output == None: self.file = open(output, "w")
        for person in self.profiles:
            print_out(person.nameLifespan(), self.file)
            reader = rememori_reader(language=self.language, name_convention=self.name_convention)
            records = reader.profile_is_matched(person)
            for obtained in records:
                print_out("  -  " + obtained.nameLifespan() + "  " + obtained.gen_data["web_ref"][0], self.file)
            reader2 = elnortedecastilla_reader(language=self.language, name_convention=self.name_convention)
            records2 = reader2.profile_is_matched(person)
            for obtained in records2:
                print_out("  -  " + obtained.nameLifespan() + "  " + obtained.gen_data["web_ref"][0], self.file)
        if not self.file == None: self.file.close()

def print_out(message, file):
    '''
    Function to be used for printing
    '''
    logging.info(message)
    if not file == None:
        file.write(message + "\n")


def accuracy_data(data):
    '''
    This functions will provide the accuracy data for input
    '''
    if "ABT" in data: return "ABOUT"
    elif "BEF" in data: return "BEFORE"
    elif "AFT" in data: return "AFTER"
    else: return "EXACT"