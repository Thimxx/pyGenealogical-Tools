__all__ = ["gedcom_profile", "gedcom_database", "gedcom_family"]

EQUIVALENCE_PROFILE = {"birth" : "BIRT", "death" : "DEAT", "baptism" : "BAPM", "burial" : "BURI", "residence" : "RESI"}
EQUIVALENCE = EQUIVALENCE_PROFILE
EQUIVALENCE["marriage"] = "MARR"
LOCATION_EQUIVALENCE = {"city" : "CITY", "state": "STAE", "country" : "CTRY"}
GEDCOM_MONTH = { 1:"JAN", 2:"FEB", 3:"MAR", 4:"APR", 5:"MAY", 6:"JUN", 7:"JUL", 8:"AUG", 9:"SEP", 10:"OCT", 11:"NOV", 12:"DEC"}

def get_date_info_from_ged(date_ged):
    '''
    This is a function that will provide the date as normal input for events
    '''
    accuracy = "EXACT"
    day_end = None
    month_end = None
    year_end = None
    formatted = date_ged.split(" ")
    if formatted[0].upper() == "BEF":
        accuracy = "BEFORE"
        day, month, year = get_date_components(date_ged.replace("BEF ", ""))
    elif formatted[0].upper() == "AFT":
        accuracy = "AFTER"
        day, month, year = get_date_components(date_ged.replace("AFT ", ""))
    elif formatted[0].upper() == "ABT":
        accuracy = "ABOUT"
        day, month, year = get_date_components(date_ged.replace("ABT ", ""))
    elif formatted[0].upper() == "BET":
        accuracy = "BETWEEN"
        new_split = date_ged[3:].split("AND")
        day, month, year =  get_date_components(new_split[0])
        day_end, month_end, year_end =  get_date_components(new_split[1])
    else:
        day, month, year =  get_date_components(date_ged)
    return year, month, day, accuracy, year_end, month_end, day_end
def get_date_components(date_string):
    '''
    This function will be used to extract the year, month and day of an string
    notice that as day or even month might be missing, this cannot be achieved
    with strptime
    '''
    day = None
    month = None
    date_divided = date_string.strip().split(" ")
    year = int(date_divided[-1:][0])
    if len(date_divided) == 3:
        day = int(date_divided[0])
        month = list(GEDCOM_MONTH.keys())[list(GEDCOM_MONTH.values()).index(date_divided[1])]
    elif len(date_divided) == 2:
        month = list(GEDCOM_MONTH.keys())[list(GEDCOM_MONTH.values()).index(date_divided[0])]
    return day, month, year