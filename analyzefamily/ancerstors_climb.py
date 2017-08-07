'''
Created on 7 ago. 2017

@author: Val
'''

class climb(object):
    '''
    This class will provide a list of ancestors growing up from the current profile
    '''


    def __init__(self, source_person):
        '''
        As input it is needed a class pyGeni.profile already obtained.
        '''
        self.source_person = source_person
        
    def get_ancestors(self, generations):
        '''
        This functions obtains the ancestors up to the requested generations.
        '''
        
    
        