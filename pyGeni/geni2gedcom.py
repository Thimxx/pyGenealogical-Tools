'''
Created on 26 mar. 2018

@author: Val
'''
#TODO: mixed families+
import logging
from pyGedcom.gedcompy_wrapper import gedcom_file
from pyGedcom.gedcom_profile import gedcom_profile
from pyGeni import profile
from messages.pygeni_messages import NUMBER_OF_PROFILES, PROCESSING

class geni2gedcom(object):
    '''
    Given a profile this module will connecto to geni and will extract all profiles
    below and generate a gedcom.
    '''
    def __init__(self, geni_profile):
        '''
        Constructor
        '''
        self.geni_profile = geni_profile
    def get_gedcom(self, output):
        '''
        This will execute and create the gedcom to be used
        '''
        #We firstly create the gedcom wrapper file
        new_gedcom = gedcom_file()
        #We execute the reccurent function
        self.added_profiles = {}
        self.introduce_family(self.geni_profile, new_gedcom)
        #We save in the output specified
        new_gedcom.save(output)
        return new_gedcom
    def introduce_family(self, init_profile, gedcom_data):
        '''
        Recursive function to introduce the family in the gedcom
        '''
        logging.info(NUMBER_OF_PROFILES + str(len(self.added_profiles.keys())) + PROCESSING + init_profile.nameLifespan())
        #Let's take first the children
        children = init_profile.children
        prof_id = init_profile.geni_specific_data["id"]
        #For the first profile we check first if the profile has been generated first
        if not isinstance(init_profile, gedcom_profile):
            #Notice that we will only go through this one a single time, as all the others
            #will be generated in the next step
            gedcom_profile.convert_gedcom(init_profile)
            gedcom_data.add_element(init_profile.individual)
            self.added_profiles[prof_id] = init_profile
        #Firstly we will create the array with all the partners in it
        children_matrix = {}
        for id_partner in init_profile.partner:
            children_matrix[id_partner] = []
        for new_id in children:
            #First thing to check is if we have already added the profile, we might
            #be in the situation of double profiles in intermarriage of descendants.
            new_prof = None
            if not (new_id in self.added_profiles.keys()):
                #Ok, if really a new profile, so we create it, we transfor it and
                #also we add to the added profiles
                new_prof = profile.profile(new_id)
                gedcom_profile.convert_gedcom(new_prof)
                gedcom_data.add_element(new_prof.individual)
                self.added_profiles[new_id] = new_prof
                #And we investigate, obviously!
                self.introduce_family(new_prof, gedcom_data)
            else:
                new_prof = self.added_profiles[new_id]
            #To avoid removing data from the profile we create a temp array using
            #the method list to avoid a linked copy
            temp_parents = list(new_prof.parents)
            temp_parents.remove(prof_id)
            children_matrix[temp_parents[0]].append(new_prof)
        #Only in case there is a partner, we include him/her!
        if (len(init_profile.partner) > 0):
            #Now let's use the partner as well, we may have several partners
            for id_partner in children_matrix.keys():
                prof_partner = None
                #First thing, we need to check the partner is already identified or not
                if (id_partner in self.added_profiles.keys()):
                    #We take the previous so!
                    prof_partner = self.added_profiles[id_partner]
                else:
                    #We get the profile data
                    prof_partner = profile.profile(id_partner)
                    #We add the profile in!
                    gedcom_profile.convert_gedcom(prof_partner)
                    #Now goes to the gedcom
                    gedcom_data.add_element(prof_partner.individual)
                    #And we mark is already in added profiles
                    self.added_profiles[id_partner] = prof_partner
                #We create here the family
                gedcom_data.create_family(init_profile, prof_partner, children_matrix[id_partner])