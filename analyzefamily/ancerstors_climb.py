'''
Created on 7 ago. 2017

@author: Val
'''
from pyGeni.immediate_family import immediate_family

class climb(object):
    '''
    This class will provide a list of ancestors growing up from the current profile
    '''


    def __init__(self, database):
        '''
        As input it is needed a database derived from common_database.
        '''
        self.database = database
    def get_ancestors(self, source_person, generations):
        '''
        This functions obtains the ancestors up to the requested generations.
        '''
        #Firstly we initiate the list which will contain all
        ancestors = []
        #The first person is always having the value first
        current_gen = [source_person.get_id()]
        ancestors.append(current_gen)
        #We introduce also a function to check duplications of profile... if they are duplicated, we take them out!
        affected_profiles = {}
        affected_profiles[source_person.get_id()] = 1
        for i in range(1, generations + 1):
            #We create an intermediate source version we will store all parents.
            next_gen = []
            #We iterate in all ancestors in this generation
            for prof_id in current_gen:
                #Now we go one, by one the parents reflecting the next generation
                ids = self.database.get_parents_from_child(prof_id)[0]
                for parent in ids:
                    #be careful with duplications!!! we will not repeat it!
                    if parent and (not parent in affected_profiles):
                        #Now we get the profile of the parents
                        next_gen.append(parent)
                        #We add it to avoid duplications later on!
                        affected_profiles[parent] = affected_profiles[prof_id]/2
                    elif parent:
                        #This means the profile is duplicated, so we add the value
                        affected_profiles[parent] = affected_profiles[parent] + affected_profiles[prof_id]/2
            #If there are no longer ancestors, we should stop!
            if len(next_gen) == 0:
                return ancestors, affected_profiles
            #Now...we append this generation to ancestors
            ancestors.append(next_gen)
            #And now the next generation is the current!!!
            current_gen = next_gen
        #We just finish delivering the ancestors back!!
        return ancestors, affected_profiles
    def get_cousins(self,source_person, generations):
        '''
        This function will create a matrix of cousins, just counting the number
        of affected cousins for a given profile.
        '''
        #We initiate an array of 0s for calculating
        cousins_count = [[0 for j in range(generations +1)] for i in range(generations +1)]
        array_of_cousins = [[0 for j in range(generations +1)] for i in range(generations +1)]
        ancestors2, profiles_scored = self.get_ancestors(source_person, generations)
        prior_profiles = list(profiles_scored.keys())
        for i in range(0, generations+1):
            cousins_count[i][i] = len(ancestors2[i])
            array_of_cousins[i][i]  = ancestors2[i]
        #We have finished the list of grand parents, now we need to go down!
        for i in range(1, generations+1):
            #We go down in the matrix, from one we get the previous
            #we are located in the top previous value! so, the first value
            #are the gran-parents of the guy!
            for j in range(i, 0,-1):
                generation_below = []
                #We need to get the children from the top guys!
                #We iterated in family items
                for parental_profile in array_of_cousins[i][j]:
                    #We analyze child by child to include in the analysis
                    for child in self.database.get_all_children(parental_profile):
                        #If the profile is not existing before, we shall include it
                        if not ( child in profiles_scored.keys()):
                            generation_below.append(child)
                            profiles_scored[child] = 0
                        if not ( (child in prior_profiles) and (parental_profile in prior_profiles) ):
                            profiles_scored[child] = profiles_scored[child] + profiles_scored[parental_profile]/2
                array_of_cousins [i][j-1] = generation_below
                cousins_count[i][j-1] = len(generation_below)
        return array_of_cousins, cousins_count, profiles_scored