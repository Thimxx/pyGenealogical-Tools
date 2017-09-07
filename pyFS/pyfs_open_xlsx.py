'''
Created on 15 ago. 2017

@author: Val
'''
import logging
from openpyxl import load_workbook
from openpyxl.utils import  column_index_from_string
from pyGenealogy.common_profile import gen_profile
from pyGenealogy.gen_utils import is_year, naming_conventions, get_children_surname, get_name_from_fullname
from datetime import datetime
from messages.pyFS_messages import NO_VALID_NAMING_CONVENTION

ignored_fields =["batch_number", "score", "role_in_record", "father_full_name", "mother_full_name"]
date_fields = ["birth_date", "burial_date", "chr_date", "residence_date", "death_date", "marriage_date"]
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
                    elif (column_criteria in date_fields):
                        #Notice that we shall detect if the given date is a year or a specific date
                        #we will make the different using "about" and using datetime in the background
                        if(is_year(cell_value)):
                            this_introduction = self.__include_a_date__(column_criteria, included_profile, datetime.strptime(cell_value, "%Y").date(), "ABOUT")
                        else:
                            this_introduction = self.__include_a_date__(column_criteria, included_profile, datetime.strptime(cell_value, "%d %b %Y").date(), "EXACT")
                    elif(column_criteria == "full_name"):
                        #TODO:Better replace by a method call
                        included_profile.set_name(get_name_from_fullname(cell_value,potential_father_surname, potential_mother_surname))
                    elif (column_criteria in ignored_fields):
                        pass
                    else:
                        number_missing = number_missing + 1
                        print(column_criteria)
                    if (not this_introduction): included_right = False
            if(not included_right) : correct_introduction = False
            self.profiles.append(included_profile)
        return correct_introduction
    def __include_a_date__(self, column_criteria, profile, date_object, accuracy ):
        '''
        Function to avoid repetition
        '''
        if (column_criteria  == "birth_date"):
            return profile.setCheckedBirthDate(date_object, accuracy)
        elif (column_criteria  == "burial_date"):
            return profile.setCheckedBurialDate(date_object, accuracy)
        elif (column_criteria == "chr_date"):
            return profile.setCheckedBaptismDate(date_object, accuracy)
        elif (column_criteria == "residence_date"):
            return profile.setCheckedResidenceDate(date_object, accuracy)
        elif (column_criteria == "death_date"):
            return profile.setCheckedDeathDate(date_object, accuracy)