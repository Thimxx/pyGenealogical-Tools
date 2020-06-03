'''
Created on 16 sept. 2017

@author: Val
'''
import re
from langdetect import detect
from geotext import GeoText


__all__ = ["pyrememori","pyvocento", "pygenanalyzer", "pyabc", "pyCommonRegisters", "pyesquelas",
           "pycementry_valencia","pylavanguardia", "get_location_from_text", "sp_age_location_colector"]

used_strings = {
    "es" : {"AT AGE" : " a los ", "AT THE AGE" : " a la edad de ", "YEARS" : " años"},
    "ca" : { "AT AGE" : " als ", "AT THE AGE" : " a l'edat de ", "YEARS" : " anys"}
    }

def get_location_from_text(text):
    '''
    This function will provide the location from the text
    '''
    result = GeoText(text).cities
    if len(result) > 0:
        return result[0]
    return None

def sp_age_location_colector(data, language = "es", detect_lan = False):
    '''
    This is a common function to be used in several parsers which provides
    the location and age from a data source
    '''
    if detect_lan:
        language_temp = detect(data)
        if language_temp in used_strings.keys(): language = language_temp
    str_input = used_strings[language]
    age = None
    if  (str_input["AT AGE"] in data) and (str_input["YEARS"] in data):
        result = re.search(str_input["AT AGE"] + '(.*)' + str_input["YEARS"], data)
        if result:
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    elif (str_input["AT AGE"] in data):
        result = re.search(str_input["AT AGE"] + '(.*)' + str_input["YEARS"], data)
        if not (result is None):
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    elif  (str_input["AT THE AGE"] in data):
        result = re.search(str_input["AT THE AGE"] + '(.*)' + str_input["YEARS"], data)
        if result is not None:
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    location = None
    if location: location = re.split(" |,|[.]", location)[0]
    #For location we will use the function get_location
    location = get_location_from_text(data)
    return location, age