'''
Created on 16 sept. 2017

@author: Val
'''
import re
from langdetect import detect

__all__ = ["pyrememori","pyelnortedecastilla", "pygenanalyzer", "pyabc", "pyCommonRegisters", "pyesquelas", "pycementry_valencia", "pylavanguardia"]

used_strings = {
    "es" : {"IN" : "en ", "AT AGE" : " a los ", "AT THE AGE" : " a la edad de ", "YEARS" : " años"},
    "ca" : {"IN"  : " a ", "AT AGE" : " als ", "AT THE AGE" : " a l'edat de ", "YEARS" : " anys"}
    }

def sp_age_location_colector(data, language = "es", detect_lan = False):
    '''
    This is a common function to be used in several parsers which provides
    the location and age from a data source
    '''
    if detect_lan:
        language_temp = detect(data)
        if language_temp in used_strings.keys(): language = language_temp
    str_input = used_strings[language]
    location = None
    age = None
    if ((str_input["IN"] in data) and (str_input["AT AGE"] in data)):
        result = re.search(str_input["IN"] +'(.*)' + str_input["AT AGE"], data)
        if not (result == None):
            location = result.group(1).strip()
        result = re.search(str_input["AT AGE"] + '(.*)' + str_input["YEARS"], data)
        if not (result == None):
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    elif ((str_input["IN"] in data) and (str_input["AT THE AGE"] in data)):
        result = re.search(str_input["IN"] +'(.*)' + str_input["AT THE AGE"], data)
        if not (result == None):
            location = result.group(1).strip()
        result = re.search(str_input["AT THE AGE"] + '(.*)' + str_input["YEARS"], data)
        if not (result == None):
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    elif (str_input["IN"] in data):
        location = data.split(str_input["IN"],1)[1].strip()
    elif  (str_input["AT AGE"] in data) and (str_input["YEARS"] in data):
        result = re.search(str_input["AT AGE"] + '(.*)' + str_input["YEARS"], data)
        if result:
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    if location: location = re.split(" |,|[.]", location)[0]
    return location, age