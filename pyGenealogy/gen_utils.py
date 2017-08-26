'''
Created on 26 ago. 2017

@author: Val
'''
import logging
from messages.pyGenealogymessages import NO_VALID_CONVENTION

naming_conventions = ["father_surname", "spanish_surname"]

def is_year(my_potential_year):
    '''
    A simple module to detect if a given string is a year. Notice than when using
    datetime module is not possible to make the difference and detect if 1894 is just
    a year compared to 1st Jan 1894 when using strptime
    '''
    try: 
        year = int(my_potential_year)
        if year > 2990: return False
        return True
    except ValueError:
        return False

#TODO: include further naming conventions
def get_children_surname(father_surname, mother_surname, selected_convention):
    '''
    Simple function that provides the surname of children given the surname of 
    both parents
    '''
    if (selected_convention == "father_surname"):
        return father_surname
    elif (selected_convention == "spanish_surname"):
        return father_surname + " " + mother_surname
    else:
        logging.error(NO_VALID_CONVENTION) 
        return ""

def get_name_from_fullname(full_name, list_father_surnames, list_mother_surnames):
    '''
    Given a full name, including surname, this function will provide out the first name of
    the person removing the surname of the person
    '''
    name_string = full_name
    merged_list = list_father_surnames + list_mother_surnames
    for surname in merged_list:
        name_string = name_string.replace(" " + surname, "")
    return name_string