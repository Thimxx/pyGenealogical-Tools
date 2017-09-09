'''
Created on 15 ago. 2017

@author: Val
'''
import logging
from openpyxl import load_workbook
from openpyxl.utils import  column_index_from_string
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import is_year, naming_conventions, get_children_surname, get_name_from_fullname, get_partner_gender
from datetime import datetime
from messages.pyFS_messages import NO_VALID_NAMING_CONVENTION, NO_VALID_DATA_FIELD, ENDED
from pyGeni import profile
from pyGenealogy import NOT_KNOWN_VALUE


ignored_fields =["batch_number", "score", "role_in_record", "father_full_name", "mother_full_name"]
date_fields = {"birth_date" : "birth_date" , "burial_date" : "burial_date", "chr_date" : "baptism_date", 
               "residence_date" : "residence_date", "death_date" : "death_date", "marriage_date" : "marriage_date"}
LOCATION_EQUIVALENCE = {"death_place_text" : "death_place", "residence_place_text" : "residence_place",
                        "chr_place_text" : "baptism_place", "marriage_place_text" : "marriage_place"}

class getFSfamily(object):
    '''
    This class reads the  FS output excel from the website of FamilySearch
    '''
    def __init__(self, filename, naming_convention = "father_surname", language = "en"):
        '''
        This contructor reads the output file from FS in xlsx format
        '''
        #TODO: include further naming conventions
        self.correct_execution = True
        self.language = language
        if (not naming_convention in naming_conventions):
            logging.error(NO_VALID_NAMING_CONVENTION) 
            self.correct_execution = False
        self.naming_convention = naming_convention
        self.loaded_data = load_workbook(filename, data_only=True)
        if (not self.__locate_key_fields__()): self.correct_execution = False
        self.profiles = []
        self.geni_profiles = []
        self.related_profiles = {}
        self.related_geni_profiles = []
        self.parents_profiles = {}
        self.parents_geni_profiles = []
        self.__get_profiles__()
    def __locate_key_fields__(self):
        '''
        This function is used to locate the key areas within the file in order to later
        on filter
        '''
        for sheet in self.loaded_data:
            for row in sheet.iter_rows():
                for cell in row:
                    #Ok, we are looking for the right location and usually the first line contains score
                    if(cell.internal_value == "score"):
                        self.sheet_title = sheet.title
                        self.initial_row = cell.row
                        self.initial_column = cell.column
                        return True
        return False
    #TODO: simplify including intermediate functions
    def __get_profiles__(self):
        '''
        This function will take all different profiles included inside the excel file
        '''
        current_sheet = self.loaded_data[self.sheet_title]
        #Iterator of missing inptus
        number_missing = 0
        #The id number to be used
        id_profiles = 0
        #Temporal variable checking the correct reading
        correct_introduction = True
        #Intermediate variables for potential surnames in the input file
        potential_father_surname = []
        potential_father_surname_repetitions = []
        potential_mother_surname = []
        potential_mother_surname_repetitions = []
        #We firstly detect the surnames of the parents of the profile,we cannot avoid the double
        #iteration
        for row in range(self.initial_row+1, self.loaded_data[self.sheet_title].max_row+1):
            for column_index in range(column_index_from_string(self.initial_column),self.loaded_data[self.sheet_title].max_column):
                column_criteria = current_sheet.cell(row=self.initial_row, column=column_index).value
                cell_value = current_sheet.cell(row=row, column=column_index).value
                cell_value_splitted = []
                surname = ""
                if (isinstance(cell_value,str)):
                    cell_value_splitted = cell_value.split(" ")
                    surname = cell_value_splitted[-1]
                if ( len(cell_value_splitted) > 1 ): 
                    #We are only interested in the 
                    if(column_criteria == "father_full_name"):
                        if (not surname in potential_father_surname):
                            potential_father_surname.append(surname)
                            potential_father_surname_repetitions.append(1)
                        else:
                            index = potential_father_surname.index(surname)
                            potential_father_surname_repetitions[index] = potential_father_surname_repetitions[index] + 1
                    elif(column_criteria == "mother_full_name"):
                        if (not surname in potential_mother_surname):
                            potential_mother_surname.append(surname)
                            potential_mother_surname_repetitions.append(1)
                        else:
                            index = potential_mother_surname.index(surname)
                            potential_mother_surname_repetitions[index] = potential_mother_surname_repetitions[index] + 1
        index_father_surname = potential_father_surname_repetitions.index(max(potential_father_surname_repetitions))
        index_mother_surname = potential_mother_surname_repetitions.index(max(potential_mother_surname_repetitions))
        father_surname = potential_father_surname[index_father_surname]
        mother_surname = potential_mother_surname[index_mother_surname]
        children_surname = get_children_surname(father_surname, mother_surname, self.naming_convention)
        #Now we read the complete file
        for row in range(self.initial_row+1, self.loaded_data[self.sheet_title].max_row+1):
            included_profile = gen_profile("TBD", children_surname)
            included_right = True
            for column_index in range(column_index_from_string(self.initial_column),self.loaded_data[self.sheet_title].max_column):
                column_criteria = current_sheet.cell(row=self.initial_row, column=column_index).value
                cell_value = current_sheet.cell(row=row, column=column_index).value
                #We are ignoring all those cells that are empty.
                if ( cell_value ): 
                    this_introduction = True
                    #Ok, now we go one by one each of the different values
                    if(column_criteria == "gender"):
                        this_introduction = included_profile.setCheckedGender(cell_value)
                    elif (column_criteria in LOCATION_EQUIVALENCE.keys()):
                        included_profile.setPlaces(LOCATION_EQUIVALENCE[column_criteria], cell_value, self.language)
                    elif (column_criteria == "person_url"):
                        included_profile.setWebReference("https://familysearch.org/" +cell_value)
                    elif (column_criteria in date_fields.keys()):
                        #Notice that we shall detect if the given date is a year or a specific date
                        #we will make the different using "about" and using datetime in the background
                        if(is_year(cell_value)):
                            this_introduction = self.__include_a_date__(column_criteria, included_profile, datetime.strptime(cell_value, "%Y").date(), "ABOUT")
                        else:
                            this_introduction = self.__include_a_date__(column_criteria, included_profile, datetime.strptime(cell_value, "%d %b %Y").date(), "EXACT")
                    elif(column_criteria == "full_name"):
                        #TODO:Better replace by a method call
                        included_profile.set_name(get_name_from_fullname(cell_value,potential_father_surname, potential_mother_surname))
                    elif (column_criteria == "spouse_full_name"):
                        #Here we create a new profile using the surname of the guy
                        names = cell_value.split(" ")
                        partner = gen_profile(" ".join(names[:-1]), names[-1])
                        partner.set_id(id_profiles)
                        included_profile.set_marriage_id_link(id_profiles)
                        self.related_profiles[id_profiles] = partner
                    elif (column_criteria == "other_full_names"):
                        #The separator provided by family search is semicolumn
                        parents = cell_value.split(";")
                        #We go for the father
                        if (len(parents[0].split(" ")) > 1):
                            #Ok, we have 2 surnames
                            father = gen_profile(" ".join(parents[0].split(" ")[:-1]), parents[0].split(" ")[-1])
                        else:
                            father = gen_profile(parents[0], NOT_KNOWN_VALUE)
                        #Now, the mother
                        if (len(parents[1].split(" ")) > 1):
                            #Ok, we have 2 surnames
                            mother = gen_profile(" ".join(parents[1].split(" ")[:-1]), parents[1].split(" ")[-1])
                        else:
                            mother = gen_profile(parents[1], NOT_KNOWN_VALUE)
                        father.setCheckedGender("M")
                        mother.setCheckedGender("F")
                        self.parents_profiles[id_profiles] = [father, mother]
                    elif (column_criteria in ignored_fields):
                        pass
                    else:
                        number_missing = number_missing + 1
                        print(column_criteria)
                    if (not this_introduction): included_right = False
                #This is a way to later on identify the link between the profiles
            id_profiles += 1
            if(not included_right) : correct_introduction = False
            self.profiles.append(included_profile)
        return correct_introduction
    def __include_a_date__(self, column_criteria, profile, date_object, accuracy ):
        '''
        Function to avoid repetition
        '''
        if (column_criteria in date_fields.keys()):
            return profile.setCheckedDate(date_fields[column_criteria], date_object, accuracy)
        else:
            logging.error(NO_VALID_DATA_FIELD + column_criteria)
            return False
    
    def create_profiles_in_Geni(self, token, geni_data):
        '''
        This method will create the needed profiles directly in Geni
        '''
        for profile_obtained in self.profiles:
            logging.info(profile_obtained.returnFullName())
            profile.profile.create_as_a_child(profile_obtained, token, geni_input=geni_data )
            self.geni_profiles.append(profile_obtained)
            logging.info(profile_obtained.geni_specific_data["url"])
            if profile_obtained.gen_data.get("marriage_link", None) in self.related_profiles.keys():
                id_of_marriage = profile_obtained.gen_data["marriage_link"]
                partner = self.related_profiles[id_of_marriage]
                #It is a partner so we add as opposite sex!
                partner.setCheckedGender(get_partner_gender(profile_obtained.gen_data["gender"]))
                partner.setWebReference(profile_obtained.gen_data["web_ref"])
                profile.profile.create_as_a_partner(partner, token, geni_input=profile_obtained.geni_specific_data["id"],
                                                    type_geni="" )
                partner.setCheckedDate("marriage_date", profile_obtained.gen_data["marriage_date"], profile_obtained.gen_data["accuracy_marriage_date"]  )
                self.related_geni_profiles.append(partner)
                logging.info(partner.geni_specific_data["url"])
                print(partner.geni_specific_data["id"])
                print(id_of_marriage, self.parents_profiles.keys(), partner.geni_specific_data["id"])
                if id_of_marriage in self.parents_profiles.keys():
                    father = self.parents_profiles[id_of_marriage][0]
                    mother = self.parents_profiles[id_of_marriage][1]
                    father.setWebReference(profile_obtained.gen_data["web_ref"])
                    mother.setWebReference(profile_obtained.gen_data["web_ref"])
                    if (father.gen_data["surname"] == NOT_KNOWN_VALUE):
                        #Ok the data was not including the right data, but we know the surname
                        father.gen_data["surname"] = partner.gen_data["surname"]
                    profile.profile.create_as_a_parent(father, token, geni_input=partner.geni_specific_data["id"], type_geni="" )
                    profile.profile.create_as_a_parent(mother, token, geni_input=partner.geni_specific_data["id"], type_geni="" )
                    self.parents_geni_profiles.append(father)
                    self.parents_geni_profiles.append(mother)
        logging.info(ENDED)