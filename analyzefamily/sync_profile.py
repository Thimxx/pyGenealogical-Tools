'''
Created on 1 jun. 2020

@author: Val
'''

from analyzefamily import continue_execution_step, print_out, record_research_log
from pyGenealogy.generic_functions import get_research_log_id
from datetime import datetime
from pyGenealogy import ARRAY_EVENTS
from messages.pygenanalyzer_messages import SYNC_NEW_EVENT, SYNC_IN_DB

MATCH = "_SYNC"
STATUS_SYNC = "SYNC="

class sync_profiles(object):
    '''
    This class is a synchronizer of the data of 2 profiles, it makes sure the profiles
    have the same values, copying the missing data from one to the other
    '''
    def __init__(self, database_primary, database_secondary, data_language="en", name_convention="father_surname"):
        '''
        It gets as inputs:
        - database_primary: is derived function of common_database which will store the recording of the comparison
        - database_seconday: is derived function of common_database which is an external source for data
        - data_language: is the expected data languages as standards
        - name_convention: is the convention of inheriting surnames between families
        '''
        self.dbp = database_primary
        self.dbs = database_secondary
        self.data_language = data_language
        self.name_convention = name_convention
    def execute_sync(self, profiles2analyze = "all", threshold = 360, storage = False):
        '''
        This is the core function, it will execute the global sync of profiles Between
        primary and secondary database
        '''
        list_prof = self.dbp.get_all_profiles()
        if profiles2analyze != "all": list_prof = self.dbp.get_several_profile_by_ID(profiles2analyze).values()
        kind_match = self.dbs.get_db_kind()
        match_str = str(kind_match) + MATCH
        for prof in list_prof:
            if prof.get_specific_web(kind_match) and continue_execution_step(prof, match_str, STATUS_SYNC, threshold = threshold):
                #Obtain the secondary database profile needed
                prof_second = self.dbs.get_profile_by_ID(prof.get_specific_web(kind_match)["url"])
                #We obtain the latest update time
                update_primary   = (datetime.now() - prof.get_update_datetime())
                update_secondary = (datetime.now() - prof_second.get_update_datetime())
                minimum_diff = min(update_primary.days, update_secondary.days)
                #Now, we only review in case the modification date is recent or there has not been any review before
                if (prof.get_research_item_by_name(match_str) is None) or minimum_diff < threshold:
                    #We inform by the command line that we are analyzing one profile
                    print_out(str(prof.get_id()) + " : "  + prof.nameLifespan())
                    #We check all the events of the profile in the dictionary
                    events_primary = prof.getEventsDict()
                    events_secondary = prof_second.getEventsDict()
                    events_in_both = set(events_primary) & set(events_secondary)
                    events_only_in_primary = set(events_primary).difference(set(events_secondary))
                    events_only_in_secondary = set(events_secondary).difference(set(events_primary))
                    sync_data = { "PRIM" : { "prof_destination" : prof,
                                             "events2introduce" : events_only_in_secondary,
                                             "events_dict"      : events_secondary,
                                             "db_destiny"       : self.dbp},
                                  "SEC" : {  "prof_destination": prof_second,
                                             "events2introduce" : events_only_in_primary,
                                             "events_dict"      : events_primary,
                                             "db_destiny"       : self.dbs}
                                }
                    for id_sync in sync_data:
                        #As we know, we iterate on those events we know we need to intoduce
                        for event_id in sync_data[id_sync]["events2introduce"]:
                            if event_id in ARRAY_EVENTS:
                                print_out("NOT IMPLEMENTED FOR " + event_id)
                            else:
                                #We obtain the new event class
                                print_out(SYNC_NEW_EVENT + event_id + SYNC_IN_DB + sync_data[id_sync]["db_destiny"].get_db_kind())
                                event_new = sync_data[id_sync]["events_dict"][event_id]
                                sync_data[id_sync]["prof_destination"].setNewEvent( event_new )
                    #We store teh exercise performed
                    loc_research = get_research_log_id(prof, storage = storage)
                    today = datetime.now().toordinal()
                    notes_toadd = STATUS_SYNC + str(today)
                    record_research_log(prof, match_str, loc_research, "", notes_toadd)