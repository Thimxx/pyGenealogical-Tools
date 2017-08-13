'''
Created on 8 ago. 2017

@author: Val
'''

class geni_union:
    '''
    This function deals with geni unions model, it is a data handler, no itended
    to be used as a caller.
    '''


    def __init__(self, union_dict, union_id):
        '''
        This constructor takes a dictionary taken from geni website
        '''
        self.union_id = union_id
        self.union_url = union_dict["url"]
        self.union_status = union_dict["status"]
        #We create temporal profiles for teh parents and children
        self.parents = []
        self.children = []
        for tmp_profile in union_dict["edges"]:
            if (union_dict["edges"][tmp_profile]['rel'] == "child"):
                self.children.append(tmp_profile)
            else:
                self.parents.append(tmp_profile)
    def is_profile_child(self, profile2check):
        '''
        Simple function that checks if the given profile is a child inside the union
        '''
        return profile2check in self.children
    def is_profile_parent(self, profile2check):
        '''
        Simple function that checks if the given profile is a parent inside the union
        '''
        return profile2check in self.parents