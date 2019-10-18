'''
Created on 16 sept. 2017

@author: Val
'''
import re

__all__ = ["pyrememori","pyelnortedecastilla", "pygenanalyzer", "pyabc", "pyCommonRegisters", "pyesquelas", "pycementry_valencia"]

def sp_age_location_colector(data):
    '''
    This is a common function to be used in several parsers which provides
    the location and age from a data source
    '''
    location = None
    age = None
    if (("en" in data) and ("a los" in data)):
        result = re.search('en(.*)a los', data)
        if not (result == None):
            location = result.group(1).strip()
        result = re.search('a los(.*)años', data)
        if not (result == None):
            aged = result.group(1).strip()
            if aged.isdigit(): age = int(result.group(1).strip())
    elif ("en" in data):
        location = data.split("en",1)[1].strip()
    elif  ("a los" in data) and ("años" in data):
        result = re.search('a los(.*)años', data)
        aged = result.group(1).strip()
        if aged.isdigit(): age = int(result.group(1).strip())
    if location: location = re.split(" |,|[.]", location)[0]
    return location, age