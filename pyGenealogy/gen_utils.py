'''
Created on 26 ago. 2017

@author: Val
'''
import logging
from messages.pyGenealogymessages import NO_VALID_CONVENTION, NO_VALID_ACCURACY
from messages.pyGenealogymessages import NO_VALID_BIRTH_DATE, NO_VALID_DEATH_DATE, NO_VALID_DEATH_AND_BURIAL
from datetime import date
from pyGenealogy import VALUES_ACCURACY
from metaphone import doublemetaphone
from Levenshtein import jaro
import math
import requests
import pyGenealogy, os


DATA_FOLDER = os.path.join(os.path.dirname(pyGenealogy.__file__), "data")

GOOGLE_GEOLOCATION_ADDRESS = "https://maps.googleapis.com/maps/api/geocode/json?"

LOCATION_KEYS = ["place_name", "city", "county", "state", "country"]

naming_conventions = ["father_surname", "spanish_surname"]

LANGUAGES_ADDS = {"en" : [], "es" : ["de", "la", "del",  "los", "las"]}

LANGUAGES_NEXUS = {"en" : ["and"], "es" : ["y"]}

LANGUAGES_FILES = { "es" : {"surname" : "surname_es.txt", "name" : "names_es.txt", "normalize" : {"á" : "a", "é" : "e", "í" : "i", "ó" : "o", "ú" : "u", "ñ": "n", "b":"v"}}}

LANGUAGES_DATA = {}

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
def get_name_from_fullname(full_name, list_father_surnames, list_mother_surnames, language="en"):
    '''
    Given a full name, including surname, this function will provide out the first name of
    the person removing the surname of the person
    '''
    merged_list = list_father_surnames + list_mother_surnames
    for surname in merged_list:
        temp_surname = surname.split(" ")
        if len(temp_surname) > 1:
            for i in range(len(temp_surname)):
                if temp_surname[i] in LANGUAGES_ADDS[language]:
                    temp_surname[i] = ""
            new_surname = " ".join(temp_surname).rstrip().strip()
            if (not new_surname in merged_list): merged_list.append(new_surname)
    merged_metaphore = []
    for data in merged_list:
        if adapted_doublemetaphone(data, language) not in merged_metaphore:
            merged_metaphore.append(adapted_doublemetaphone(data, language))
    
    full_name_list = get_splitted_name_from_complete_name(full_name, language)
    for i, value in enumerate(full_name_list[0]):
        #We remove from the specific particle the particles from each language that are used inside surnames
        #to connect
        check_surname = value.split(" ")
        if len(check_surname) > 1:
            for j, value in enumerate(check_surname):
                if (check_surname[j].lower() in LANGUAGES_ADDS[language]):
                    check_surname[j] = ""
        adapted_surname = "".join(check_surname).rstrip()
        if (adapted_doublemetaphone(value, language) in merged_metaphore) or (adapted_doublemetaphone(adapted_surname, language) in merged_metaphore):
            full_name_list[0][i] = ""
    return " ".join(full_name_list[0]).rstrip()
def adapted_doublemetaphone(data, language="en"):
    '''
    Adapted function to take into account specific topics not considered in original version
    it accepts both strings and lists of strings
    '''
    if (type(data) == str):
        list_data = [data]
        using_string = True
    else:
        list_data = data
        using_string = False
    #We perform the operation ina list, and then we return the result
    result = []
    for data2met in list_data:
        if (language == "es"):
            #In spanish b and v are pronunced equally, if we know the language is spanish we shall remove!
            result.append(doublemetaphone(data2met.lower().replace("v", "b")))
        result.append(doublemetaphone(data2met))
    if using_string:
        return result[0]
    else:
        return result
def checkDateConsistency(birth_date, residence_date, baptism_date, marriage_date, death_date, burial_date,
                         accuracy_birth = "EXACT", accuracy_residence = "EXACT", accuracy_baptism = "EXACT", 
                         accuracy_marriage = "EXACT", accuracy_death = "EXACT", accuracy_burial = "EXACT"):
    '''
    Checker of the different dates are consistent
    '''
    #birth date is always the earliest date
    dates_death_check = []
    dates_birth_check = []
    burial_death = []
    #If there is no birth date included there is no need for the check
    if (birth_date != None):
        dates_birth_check.append(birth_date)
        check_dates_in_birth = [residence_date, baptism_date, marriage_date, death_date, burial_date]
        accuracy_in_birth = [accuracy_residence, accuracy_baptism, accuracy_marriage, accuracy_death, accuracy_burial]
        for index in range(0, len(check_dates_in_birth)):
            if (check_dates_in_birth[index] != None):
                if (accuracy_in_birth[index] == "ABOUT"):
                    #If we have an "about" the event has been around that year, with some margin, in this case, we just include
                    #the last date of the year for the check
                    dates_birth_check.append(date(check_dates_in_birth[index].year,12,31))
                else:
                    dates_birth_check.append(check_dates_in_birth[index])
        #Now we check here the data consistency
        if(min(dates_birth_check) < birth_date):
            logging.error(NO_VALID_BIRTH_DATE) 
            return False
    #Burial and Death dates are the latests ones
    if (burial_date != None): 
        if (accuracy_burial == "ABOUT"):
            burial_death.append(date(burial_date.year,12,31))
        else:
            burial_death.append(burial_date)
    if (death_date != None):
        intermediate_death = death_date  
        if (accuracy_death == "ABOUT"):
            intermediate_death = date(death_date.year,1,1)
        burial_death.append(intermediate_death)
        #Burial is never before than death date... unless in vampires, but out of scope
        if (intermediate_death > min(burial_death)):
            logging.error(NO_VALID_DEATH_AND_BURIAL)
            return False
    if ( len(burial_death) > 0):
        check_dates_in_db = [residence_date, baptism_date, marriage_date]
        accuracy_in_db = [accuracy_residence, accuracy_baptism, accuracy_marriage]
        for index in range(0, len(check_dates_in_db)):
            if (check_dates_in_db[index] != None):
                if (accuracy_in_db[index] == "ABOUT"):
                    #If we have an "about" the event has been around that year, with some margin, in this case, we just include
                    #the first date of the  year
                    dates_death_check.append(date(check_dates_in_db[index].year,1,1))
                else:
                    dates_death_check.append(check_dates_in_db[index])
        #Now we check here the data consistency
        if (len(dates_death_check) > 0):
            if (max(dates_death_check) > max(burial_death)):
                logging.error(NO_VALID_DEATH_DATE) 
                return False
    return True
def getBestDate(date1, accuracy1, date2, accuracy2):
    '''
    This method takes 2 dates with their accuracy and returns the most probable
    date
    '''
    #TODO: we need to change the model fo the data to allow the inclusion of 2 values
    #in such case we will have the possibility of having before and after
    #Wrong accuracy provided will provide None data
    if (not accuracy1 in VALUES_ACCURACY) or (not accuracy2 in VALUES_ACCURACY):
        logging.error(NO_VALID_ACCURACY) 
        return None, None
    #If we have an exact date, that's the one!
    if (accuracy1 == "EXACT"):
        return date1, accuracy1
    elif (accuracy2 == "EXACT"):
        return date2, accuracy2
    #Ok, now AFTER or BEFORE becomes more precise
    if (accuracy1 in ["BEFORE", "AFTER"]):
        return date1, accuracy1
    elif (accuracy2 in ["BEFORE", "AFTER"]):
        return date2, accuracy2
    else:
        #The only option is having 2 abouts... we get the middle value
        newyear = int((date1.year +date2.year)/2)
        return date(newyear,1,1), accuracy1
def get_formatted_location(location_string, language="en"):
    '''
    This function will provide a standard location based on google maps service
    online
    '''
    output = {}
    output["raw"] = location_string
    url = GOOGLE_GEOLOCATION_ADDRESS + "language=" + language + "&address=" + location_string
    r = requests.get(url)
    data = r.json()
    if (data["status"] == "OK"):
        #Received data is ok, we can proceed
        for result_input in data["results"][0].keys():
            if(result_input == "geometry"):
                #As we got the location details, let's get them
                output["latitude"] = data["results"][0]["geometry"]["location"]["lat"]
                output["longitude"] = data["results"][0]["geometry"]["location"]["lng"]
            elif(result_input == "address_components"):  
                #This is the data of the name of the location
                for level in  data["results"][0]["address_components"]:
                    if "locality" in level["types"]: output["city"] = level["long_name"]
                    elif "administrative_area_level_2" in level["types"]: output["county"] = level["long_name"]
                    elif "administrative_area_level_1" in level["types"]: output["state"] = level["long_name"]
                    elif "country" in level["types"]: output["country"] = level["long_name"]
    else:
        return None 
    if (not location_string.split(",")[0] in output.values()):
        final_input = []
        for particle in location_string.split(",")[0].split(" "):
            if (particle.lower() in LANGUAGES_ADDS[language]):
                final_input.append(particle.lower())
            else:
                final_input.append(particle.lower().title())
        output["place_name"] = " ".join(final_input).rstrip()
    return output
def get_partner_gender(gender):
    '''
    Simple function, it provides the opposite sex
    '''
    if ( gender == "M"): return "F"
    elif( gender == "F"): return "M"
    else: return None
def get_name_surname_from_complete_name(complete_name, convention="father_surname", language="en"):
    '''
    This function provides name and surname from a given name
    '''
    if convention in naming_conventions:
        name_split, data_identified = get_splitted_name_from_complete_name(complete_name, language=language)
        surnames = -1
        #We might receive a spanish surname wihtout 2 surnames!
        if ( convention == "spanish_surname" and len(name_split) > 2): surnames = -2
        if ("S" in data_identified) or ("N" in data_identified):
            if data_identified[-1] in ["N", "U"]:
                surnames = 0
            elif (surnames == -2) and (data_identified[-2] in ["N", "U"]):
                surnames = -1
        if (("NS" in data_identified) or ("N" in data_identified) or ("U" in data_identified)) and (len(name_split) == 1):
            surnames = 0
        if (surnames == 0):
            name = " ".join(name_split).rstrip()
            surname = ""
        else:    
            name = " ".join(name_split[:surnames]).rstrip()
            surname = " ".join(name_split[surnames:]).rstrip()
        return name,surname
    else: return None, None
def get_splitted_name_from_complete_name(complete_name, language="en", include_particle=True):
    '''
    This functions will take an string with the complete name and will
    break it into a list grouping name, surname(s).
    '''
    name_split = complete_name.rstrip().split()
    places_2_join = []
    name_category = []
    for i, particle in enumerate(name_split):
        #Let's check if the particle is containing data for next
        if particle.lower() in LANGUAGES_ADDS.get(language, []):
            if (include_particle):
                name_split[i] = particle.lower()
            else:
                name_split[i] = ""
            places_2_join.append(i)
            name_category.append("")
        elif particle.lower() in LANGUAGES_NEXUS.get(language, []):
            name_split[i] = ""
            places_2_join.append(i)
            name_category.append("")
        else:
            #Secure the data is correct
            name = get_compared_data_file(particle, language=language, data_kind = "name")
            surname = get_compared_data_file(particle, language=language, data_kind = "surname")
            if (name[1] + surname[1] == -2):
                #The data is not found in any of the lists
                name_split[i] = particle.lower().title()
                name_category.append("U")
            elif (name[1] > surname[1]): 
                name_split[i] = name[0].rstrip()
                name_category.append("N")
            elif (surname[1] > name[1]): 
                name_split[i] = surname[0].rstrip()
                name_category.append("S")
            else:
                name_split[i] = name[0].rstrip()
                name_category.append("NS")
    #name_split[i:i+2] = [" ".join(name_split[i:i+2])]
    for i in reversed(places_2_join):
        name_split[i:i+2] = [" ".join(name_split[i:i+2])]
        name_category[i:i+2] = ["".join(name_category[i:i+2])]
    return name_split, name_category

def get_compared_data_file(data, language="en", data_kind = "surname"):
    '''
    This function will compare the given name with the current data input
    '''
    if language in LANGUAGES_FILES.keys():
        if data_kind in LANGUAGES_FILES[language].keys():
            data_in_met = adapted_doublemetaphone(data, language=language)
            total_data = []
            for word, met_value in LANGUAGES_DATA[language][data_kind].items():
                if met_value == data_in_met:
                    total_data.append(word)
            #If the value is already available, we just return it
            if data in LANGUAGES_DATA[language][data_kind].keys():
                return data, 1.0
            else:
                data_temp = data.lower()
                norm = LANGUAGES_FILES[language]["normalize"]
                for notnorm in norm.keys():
                    data_temp = data_temp.replace(notnorm, norm[notnorm])
                results = {}
                for candidate in total_data:
                    candidate_temp = candidate.lower()
                    for notnorm in norm.keys():
                        candidate_temp = candidate_temp.replace(notnorm, norm[notnorm])
                    results[candidate] = jaro(candidate_temp, data_temp)
                if (any(results)):
                    return max(results, key=results.get), max(results.values())
                else:
                    return data, -1.0
    return data, -1.0
    

def get_score_compare_names(name1, surname1, name2, surname2, language="en", convention="father_surname"):
    '''
    This function compares 2 names and provides an score value and a factor of the
    relative value obtained
    Surname shall be in the form of string.
    '''
    splitted_name1 = get_splitted_name_from_complete_name(name1, language=language, include_particle=False)
    splitted_name2 = get_splitted_name_from_complete_name(name2, language=language, include_particle=False)
    splitted_surname1 = get_splitted_name_from_complete_name(surname1, language=language, include_particle=False)
    splitted_surname2 = get_splitted_name_from_complete_name(surname2, language=language, include_particle=False)
    met_name1 = adapted_doublemetaphone(splitted_name1[0], language=language)
    met_name2 = adapted_doublemetaphone(splitted_name2[0], language=language)
    met_surname1 = adapted_doublemetaphone(splitted_surname1[0], language=language)
    met_surname2 = adapted_doublemetaphone(splitted_surname2[0], language=language)
    
    factor1 = get_jaro_to_list(met_name1, met_name2)
    factor2 = get_jaro_to_list(met_surname1, met_surname2, factor=0.95)
    return 2*(factor1 +factor2), factor1*factor2
        
def get_jaro_to_list(first4jaro, list4jaro, factor = 0.9):
    result = [[0 for x in range(len(list4jaro))] for y in range(len(first4jaro))]
    loc_data = 0.0
    #If loc_data =0, we take the first one
    loc_i = 0
    loc_j = 0
    for i,item in enumerate(first4jaro):
        for j,data in enumerate(list4jaro):
            result[i][j] =jaro(item[0],data[0])*jaro(item[1],data[1])
            if result[i][j]  > loc_data:
                loc_data = result[i][j]
                loc_i = i
                loc_j = j
    first2return = first4jaro[:loc_i] + first4jaro[loc_i+1 :]
    list4return = list4jaro[:loc_j] + list4jaro[loc_j+1 :]
    if (len(first2return) == 0 ) or (len(list4return) == 0 ):
        dif=abs(len(first2return) - len(list4return))
        return loc_data*loc_data*math.pow(factor, dif)
    else:
        return loc_data*loc_data*get_jaro_to_list(first2return, list4return)
    
def get_score_compare_dates(date1, accuracy1, date2, accuracy2):
    '''
    Get an score comparing 2 dates including accuracy
    '''
    diff= abs((date1-date2).days)
    if (accuracy1 == "EXACT") and (accuracy2 == "EXACT"):
        if (diff == 0):
            return 2.0, 1.0
        elif (diff < 5):
            return 1.5+0.10*(5 - diff), 0.75+0.05*(5 - diff)
        elif (diff <30):
            return 1.0+ 0.02*(30-diff), 0.5 + 0.01*(30-diff)
        else:
            return 30.0/diff, 15.0/diff
    elif ("EXACT" in [accuracy1, accuracy2]) and ("ABOUT" in [accuracy1, accuracy2]):
        if (accuracy1 == "ABOUT"):
            date3 = date(date1.year+1, date1.month, date1.day)
            date4 = date(date1.year-1, date1.month, date1.day)
            diff = min(abs((date1-date2).days), abs((date3-date2).days), abs((date4-date2).days))
        else:
            date3 = date(date2.year+1, date2.month, date2.day)
            date4 = date(date2.year-1, date2.month, date2.day)
            diff = min(abs((date1-date2).days), abs((date3-date1).days), abs((date4-date1).days))
        if (diff < 360):
            return 1.0, 1.0
        elif (diff <720):
            return 1.0- 0.25*(diff-360)/360, 1.0
        elif (diff <1440):
            return 0.75 -0.5*(diff-720)/720, 1.0 -0.5*(diff-720)/720
        else:
            return 0.25*math.pow(1440/diff,2), 0.5*math.pow(1440/diff,2)
    elif (accuracy1 == "ABOUT") and (accuracy2 == "ABOUT"):
        diff_years= abs((date1.year-date2.year))
        if (diff_years < 2):
            return 1.0, 1.0
        elif (diff_years < 5):
            return 0.5, 0.7 + (5-diff_years)/10
        elif (diff_years < 10):
            return 0.2 + 0.06*(10 - diff_years), 0.3 + 0.04*(10 -diff_years)
        else:
            return 20/(diff_years*diff_years), 30/(diff_years*diff_years)
    


for language in LANGUAGES_FILES.keys():
    if not language in LANGUAGES_DATA.keys(): LANGUAGES_DATA[language] = {}
    for data_kind in LANGUAGES_FILES[language].keys():
        if data_kind != "normalize":
            if not data_kind in LANGUAGES_DATA[language].keys(): LANGUAGES_DATA[language][data_kind] = {}
            file2use = os.path.join(DATA_FOLDER, LANGUAGES_FILES[language][data_kind])
            openedfile = open(file2use, "r", encoding = "ISO-8859-1")
            total_data = []
            for line_file in openedfile:
                value = line_file.replace("\n", "").rstrip()
                met_changed = adapted_doublemetaphone(value, language=language)
                LANGUAGES_DATA[language][data_kind][value] =  met_changed
            
 
    