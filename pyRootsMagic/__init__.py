'''
Created on 6 July 2019

@author: Val
'''

__all__ = ["pyrm_database", "rootsmagic_family", "rootsmagic_profile", "collate_temp", "return_date_from_event"]


def collate_temp(string1, string2):
    '''
    This is a fake function used to solve the problem of the RMNOCASE issue inside the database
    '''
    if string1 == string2:
        return 0
    elif string1 > string2:
        return 1
    else:
        return -1
def return_date_from_event(event_data):
    '''
    This function will provide a given a date formated into RootsMagic from a given event
    '''
    if event_data.has_date():
        init_part = "D.+"
        date1_part = get_string_from_date(event_data.get_year(), event_data.get_month(), event_data.get_day())
        mid_part = "..+"
        end_part = "00000000.."
        if event_data.get_accuracy() == "BEFORE":
            init_part = "DB+"
        elif event_data.get_accuracy() == "AFTER":
            init_part = "DA+"
        elif event_data.get_accuracy() == "BETWEEN":
            init_part = "DR+"
            end_part = get_string_from_date(event_data.get_year_end(), event_data.get_month_end(), event_data.get_day_end()) +".."
        elif event_data.get_accuracy() == "ABOUT":
            mid_part = ".C+"
        return init_part + date1_part + mid_part + end_part
    #If no data in the event we skip and return None
    return None
def get_string_from_date(year, month, day):
    '''
    Returns the needed string in the RootsMagic format
    '''
    month_str = "00"
    if month and month < 10: month_str = "0" + str(month)
    elif month: month_str = str(month)
    day_str = "00"
    if day and day < 10: day_str = "0" + str(day)
    elif day: day_str = str(day)
    
    return str(year) + month_str + day_str