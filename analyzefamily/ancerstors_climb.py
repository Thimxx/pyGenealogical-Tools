'''
Created on 7 ago. 2017

@author: Val
'''
from pyGeni.profile import profile
from pyGeni.immediate_family import immediate_family

class climb(object):
    '''
    This class will provide a list of ancestors growing up from the current profile
    '''


    def __init__(self, source_person):
        '''
        As input it is needed a class pyGeni.profile already obtained.
        '''
        self.source_person = source_person
        self.geni_token = source_person.token
        
    def get_ancestors(self, generations):
        '''
        This functions obtains the ancestors up to the requested generations.
        '''
        #Firstly we initiate the list which will contain all
        ancestors = []
        current_gen =  {self.source_person.get_id() : self.source_person.relations }
        ancestors.append(current_gen)
        
        #We introduce also a function to check duplications of profile... if they are duplicated, we take them out!
        affected_profiles = []
        affected_profiles.append(self.source_person.get_id())
        
        for i in range(1, generations + 1):
            #We create an intermediate source version we will store all parents.
            next_gen = {}
            #We iterate in all ancestors in this generation
            for prof_id in current_gen.keys():
                #Now we go one, by one the parents reflecting the next generation
                for parent in current_gen[prof_id].parents:
                    #be careful with duplications!!! we will not repeat it!
                    if not parent in affected_profiles:
                        #Now we get the profile of the parents
                        temp_im_family = immediate_family(self.geni_token, parent) 
                        next_gen[parent] = temp_im_family
                        #We add it to avoid duplications later on!
                        affected_profiles.append(parent)
            
            #If there are no longer ancestors, we should stop! 
            if len(next_gen) == 0:
                return ancestors
            #Now...we append this generation to ancestors
            ancestors.append(next_gen)
            #And now the next generation is the current!!!
            current_gen = next_gen 
            
        #We just finish delivering the ancestors back!  
        return ancestors
    
        