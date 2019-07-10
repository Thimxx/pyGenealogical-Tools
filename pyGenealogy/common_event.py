'''
Created on 8 jul. 2019

@author: Val
'''
from pyGenealogy import EVENT_TYPE, VALUES_ACCURACY
from messages.pyGenealogymessages import NO_VALID_EVENT_START, NO_VALID_EVENT_END
from pyGenealogy.gen_utils import get_formatted_location

class event_profile(object):
    '''
    This class stores the events that will be stored inside the database
    '''


    def __init__(self, event_type):
        '''
        Constructor
        '''
        if event_type in EVENT_TYPE : 
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
        if month:           self.month_end = month_end
        if day:             self.day_end = day_end
        #Consistency checkings
        if not self.accuracy in VALUES_ACCURACY: return False
        elif self.accuracy == "BETWEEN":
            if not year_end : return False
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
        