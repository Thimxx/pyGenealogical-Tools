'''
Created on 18 abr. 2020

@author: Val
'''

class qcheck():
    '''
    This class checks the quality of a given database
    '''
    def __init__(self, database):
        '''
        The database shall be a derivate version of the pyGenealogy.common_database
        data.
        '''
        self.db = database
    def execute(self):
        '''
        Will analyze and provide statement about qualify of database
        '''
        issues = 0
        issue_data = {}
        issue_data["gender"] =[]
        issue_data["existing_date"] =[]
        for profile in self.db.get_all_profiles():
            if profile.get_id() % 1000 == 0: print(profile.get_id())
            #Not known gender is an issue
            if profile.getGender() == "U": issue_data["gender"].append(profile.get_id())
            if profile.get_earliest_event_in_event_form():
                if not profile.get_earliest_event_in_event_form().get_year(): issue_data["existing_date"].append(profile.get_id())
            else: issue_data["existing_date"].append(profile.get_id())
        issues += len(issue_data["gender"])
        issues += len(issue_data["existing_date"])
        return issues, issue_data
        