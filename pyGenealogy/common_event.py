'''
Created on 8 jul. 2019

@author: Val
'''
from pyGenealogy import EVENT_TYPE, VALUES_ACCURACY
from messages.pyGenealogymessages import NO_VALID_EVENT_START, NO_VALID_EVENT_END
from pyGenealogy.gen_utils import get_formatted_location
from datetime import date
from pyGedcom import GEDCOM_MONTH
MONTH_DAYS = { 1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6:30, 7:31, 8:31, 9: 30, 10: 31, 11:30, 12:31, None:31}

class event_profile(object):
    '''
    This class stores the events that will be stored inside the database
    '''
    def __init__(self, event_type):
        '''
        Constructor
        '''
        if event_type in EVENT_TYPE:
            self.event_type = event_type
        else:
            raise ValueError(NO_VALID_EVENT_START + event_type + NO_VALID_EVENT_END)
        self._setToNullDate()
        self.location = None
    def setDate(self, year, month = None, day = None, accuracy = "EXACT", year_end = None,
                month_end = None, day_end = None):
        '''
        Introducing the date of the event, as minimum is expected that year is included
        '''
        self._setToNullDate()
        self.year = year
        if month:           self.month = month
        if day:             self.day = day
        self.accuracy = accuracy
        if year_end:        self.year_end =year_end
        if month_end:       self.month_end = month_end
        if day_end:         self.day_end = day_end
        #Consistency checkings
        if not self.accuracy in VALUES_ACCURACY: return False
        elif self.accuracy == "BETWEEN":
            if not year_end : return False
            elif self.is_first_date_lower(year, month, day, year_end, month_end, day_end) == False:
                #We make sure that the first date is the smallest
                self.year = year_end
                if month_end:           self.month = month_end
                if day_end:             self.day = day_end
                if year:                self.year_end =year
                if month:               self.month_end = month
                if day:                 self.day_end = day
        elif (self.year_end or self.month_end or self.day_end): return False
        #if everything is ok, we return True
        return True
    def _setToNullDate(self):
        '''
        Function to initiatlize a None all areas
        '''
        self.year = None
        self.month = None
        self.day = None
        #We also include the alternate timings
        self.year_end = None
        self.month_end = None
        self.day_end = None
        self.accuracy = None
    def setLocation(self, location, language="en" ):
        '''
        This function will introduce the location related to each event
        '''
        location_data = get_formatted_location(location)
        self.location = location_data
    def setParameterInLocation(self, key_value, value_introduce):
        '''
        Used to assign as single value to a location inside location
        '''
        if not self.location: self.location = {}
        self.location[key_value] = value_introduce
    def setLocationAlreadyProcessed(self, location):
        '''
        When the location is already available (for a web page) the location is easier
        '''
        self.location = location
    def is_first_date_lower(self, year, month, day, year_end, month_end, day_end):
        '''
        Checks 2 dates and confirms which one is the lower one
        '''
        #Let's check year by year
        if year < year_end:
            return True
        elif year > year_end:
            return False
        elif not (month and month_end):
            #If we do not have the month and is the same year we cannot have a date between!!!
            return None
        elif month < month_end:
            return True
        elif month > month_end:
            return False
        elif not (day and day_end):
            #We check if we have the day, of course...
            return None
        elif day < day_end:
            return True
        elif day > day_end:
            return False
        else:
            #Here the date are exactly the same... do we need a BETWEEN????
            return "Equal"
    def is_this_event_earlier_or_simultaneous_to_this(self,event):
        '''
        Confirms if the following event is earlier or at the same time as the other
        '''
        date_self = date(self.year, self.month if self.month else 1  ,self.day if self.day else 1)
        date_other = date(event.year, event.month if event.month else 12  ,event.day if event.day else (MONTH_DAYS[event.month] if event.month else 31))
        return date_self <= date_other
    def is_this_event_later_or_simultaneous_to_this(self,event):
        '''
        Confirms if the following event is later or at the same time as the other
        '''
        date_self = date(self.year, self.month if self.month else 12  ,self.day if self.day else (MONTH_DAYS[self.month] if self.month else 31))
        date_other = date(event.year, event.month if event.month else 1  ,event.day if event.day else 1)
        return date_self >= date_other
    def has_date(self):
        '''
        Small check to confirm that there is a date
        '''
        return (self.year or self.month or self.day)
    def set_geo_location(self, latitude, longitude):
        '''
        Introduce the latitude and longitude of the place of the event
        '''
        self.setParameterInLocation("latitude", latitude)
        self.setParameterInLocation("longitude", longitude)
#==================================================
#   GET METHODS
#==================================================
    def get_event_type(self):
        '''
        Just giving back the event type
        '''
        return self.event_type
    def get_year(self):
        '''
        Just provide the year
        '''
        return self.year
    def get_year_end(self):
        '''
        Just provide the year
        '''
        return self.year_end
    def get_accuracy(self):
        '''
        Get the accuracy of the value
        '''
        if (self.accuracy): return self.accuracy
        else: return None
    def get_date(self):
        '''
        Returns a date if existing
        '''
        if self.is_full_date_available(): return date(self.year, self.month, self.day)
        else: return None
    def get_location(self):
        '''
        Get the location of the event
        '''
        if (self.location): return self.location
        else: return None
    def get_month(self):
        '''
        Just provide the month
        '''
        return self.month
    def get_month_end(self):
        '''
        Just provide the month
        '''
        return self.month_end
    def get_day(self):
        '''
        Just provide the day
        '''
        return self.day
    def get_day_end(self):
        '''
        Just provide the day
        '''
        return self.day_end
    def get_gedcom_date(self):
        '''
        This function will provide a date in the format needed for format of gedcom
        '''
        return convert_date_to_gedcom_format(self.year, self.month, self.day)
    def get_gedcom_end_date(self):
        '''
        This function will provide the end date in the format of gedcom
        '''
        return convert_date_to_gedcom_format(self.year_end, self.month_end, self.day_end)
    def is_full_date_available(self):
        '''
        Returns true if the full data of the date is avialable
        '''
        return (self.year and self.month and self.day)
    def is_any_date_available(self):
        '''
        Returns true if the full data of the date is avialable
        '''
        return (self.year or self.month or self.day)
    def _get_date_for_comparison(self):
        '''
        Function for avoiding duplication of code lines
        '''
        year1 = self.year
        year1b = self.year
        if self.month:
            month1 = self.month
            month1b = self.month
        else:
            month1 = 1
            month1b = 12
        if self.day:
            day1 = self.day
            day1b = self.day
        else:
            day1 = 1
            day1b = MONTH_DAYS[month1b]
        date1 = date(year1, month1, day1)
        date1b = date(year1b, month1b, day1b)
        return date1, date1b
    def get_difference_in_days(self, other_event):
        '''
        This function will provide a difference of days between 2 different events
        '''
        date1, date1b = self._get_date_for_comparison()
        date2, date2b = other_event._get_date_for_comparison()
        #We return the minimum difference between all dates
        return (min(abs((date1-date2).days), abs((date1-date2b).days), abs((date1b-date2).days), abs((date1b-date2b).days) ))

def convert_date_to_gedcom_format(year, month, day):
    '''
    This function transforms a date in day, month and year into gedcom format
    '''
    string_day = ""
    if day:
        if day < 10: string_day = "0" + str(day) + " "
        else: string_day = str(day) + " "
    string_month = GEDCOM_MONTH.get(month, "") + " "
    string_year = ""
    if year: string_year = str(year)
    if len((string_day + string_month + string_year).strip()) == 0: return None
    else : return (string_day + string_month + string_year).strip()
    