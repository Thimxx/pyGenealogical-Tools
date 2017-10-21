'''
Created on 7 ago. 2017

@author: Val
'''
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
                        next_gen[parent] = immediate_family(parent)
                        #We add it to avoid duplications later on!
                        affected_profiles.append(parent)
            #If there are no longer ancestors, we should stop!
            if len(next_gen) == 0:
                return ancestors
            #Now...we append this generation to ancestors
            ancestors.append(next_gen)
            #And now the next generation is the current!!!
            current_gen = next_gen
        #We just finish delivering the ancestors back!!
        return ancestors, affected_profiles
    def get_cousins(self, generations):
        '''
        This function will create a matrix of cousins, just counting the number
        of affected cousins for a given profile.
        '''
        #We initiate an array of 0s for calculating
        cousins_array = [[0 for j in range(generations +1)] for i in range(generations +1)]
        cousins_count = [[0 for j in range(generations +1)] for i in range(generations +1)]
        #We need a list for checking duplications:
        affected_profiles = []
        ancestors, affected_ancestors = self.get_ancestors(generations)
        affected_profiles = affected_profiles + affected_ancestors
        for i in range(0, generations+1):
            cousins_array[i][i] = ancestors[i]
            cousins_count[i][i] = len(ancestors[i])
        #We have finished the list of grand parents, now we need to go down!
        for i in range(1, generations+1):
            #We go down in the matrix, from one we get the previous
            #we are located in the top previous value! so, the first value
            #are the gran-parents of the guy!
            for j in range(i, 0,-1):
                down_gen = {}
                #We need to get the childrens from the top guys!
                #We iterated in family items
                for family_item in cousins_array[i][j].values():
                    #Now we have the family of a single person...
                    for child in family_item.children:
                        #And now all the children of that person!
                        if not child in affected_profiles:
                            down_gen[child] = immediate_family(child)
                            #We add it to avoid duplications later on!
                            affected_profiles.append(child)
                cousins_array[i][j-1] = down_gen
                cousins_count[i][j-1] = len(down_gen)
        return cousins_array, cousins_count, affected_profiles