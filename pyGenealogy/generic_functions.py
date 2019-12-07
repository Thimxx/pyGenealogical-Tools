'''
Created on 24 nov. 2019

@author: Val
'''
from messages.pygenanalyzer_messages import RESEARCH_INFO, RESEARCH_LOG

def get_research_log_id(person, storage = False):
    '''
    '''
    log_loc = None
    if storage and (not person.get_specific_research_log(RESEARCH_LOG)):
        log_loc = person.set_task(RESEARCH_LOG, task_type=2, details=RESEARCH_INFO)
    else: log_loc = person.get_specific_research_log(RESEARCH_LOG)
    return log_loc