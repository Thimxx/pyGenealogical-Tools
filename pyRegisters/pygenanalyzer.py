'''
Created on 28 mar. 2018

@author: Val
'''
from pyRegisters.pyrememori import rememori_reader
from pyRegisters.pyelnortedecastilla import elnortedecastilla_reader
from pyRegisters.pyabc import abc_reader
import logging

class gen_analyzer(object):
    '''
    This class will accept a given GEDCOM file for later on executing all pyRegister modules, final
    output will be a description of potential matches for helping in investigation.
    '''
    def __init__(self, language = "en", name_convention= "father_surname"):
        '''
        We shall introduce teh common database included in all areas
        '''
        self.language = language
        self.name_convention = name_convention
    def execute(self, database, output = None):
        '''
        This will execute all checkings of data with other sources.
        '''
        profiles = database.get_all_profiles()
        self.file = None
        if not output == None: self.file = open(output, "w")
        print_out("Total number of profiles = " + str(len(profiles)), self.file)
        for person in profiles:
            #We write in the screen the name of the person
            print_out(str(person.get_id()) + " = "  + person.nameLifespan(), self.file)
            #REMEMORI
            reader = rememori_reader(language=self.language, name_convention=self.name_convention)
            records = reader.profile_is_matched(person)
            #Sometimes Rememori fails in a regular manner,a checking has been introduced.
            if records:
                for obtained in records:
                    print_out("  -  " + obtained.nameLifespan() + "  " + obtained.gen_data["web_ref"][0], self.file)
            #EL NORTE DE CASTILLA
            reader2 = elnortedecastilla_reader(language=self.language, name_convention=self.name_convention)
            records2 = reader2.profile_is_matched(person)
            for obtained in records2:
                print_out("  -  " + obtained.nameLifespan() + "  " + obtained.gen_data["web_ref"][0], self.file)
            #ABC
            reader3 = abc_reader(language=self.language, name_convention=self.name_convention)
            records3 = reader3.profile_is_matched(person)
            for obtained in records3:
                print_out("  -  " + obtained.nameLifespan() + "  " + obtained.gen_data["web_ref"][0], self.file)
        if not self.file == None: self.file.close()
def print_out(message, file):
    '''
    Function to be used for printing
    '''
    logging.info(message)
    if not file == None:
        file.write(message + "\n")