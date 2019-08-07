'''
Created on 26 mar. 2018

@author: Val
'''
#TODO: mixed families+
import logging
from pyGedcom.gedcom_profile import gedcom_profile
from pyGedcom.gedcom_database import db_gedcom
from pyGeni import profile
from messages.pygeni_messages import NUMBER_OF_PROFILES, PROCESSING

class geni2gedcom(object):
    '''
    Given a profile this module will connect to geni and will extract all profiles
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
        new_gedcom = db_gedcom()
        #We execute the reccurent function
        self.added_profiles = {}
        self.introduce_family(self.geni_profile, new_gedcom)
        #We save in the output specified
        new_gedcom.save_gedcom_file(output)
        return new_gedcom
    def introduce_family(self, init_profile, gedcom_db):
        '''
        Recursive function to introduce the family in the gedcom database
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
            gedcom_db.add_profile(init_profile)
            self.added_profiles[prof_id] = init_profile
        #Firstly we will create the array with all the partners in it and also with their ids in the database
        children_matrix = {}
        children_ids = {}
        for id_partner in init_profile.partner:
            children_matrix[id_partner] = []
            children_ids[id_partner] = []
        for new_id in children:
            #First thing to check is if we have already added the profile, we might
            #be in the situation of double profiles in intermarriage of descendants.
            new_prof = None
            if not (new_id in self.added_profiles.keys()):
                #Ok, if really a new profile, so we create it, we transfor it and
                #also we add to the added profiles
                new_prof = profile.profile(new_id)
                gedcom_profile.convert_gedcom(new_prof)
                gedcom_db.add_profile(new_prof)
                self.added_profiles[new_id] = new_prof
                #And we investigate, obviously!
                self.introduce_family(new_prof, gedcom_db)
            else:
                new_prof = self.added_profiles[new_id]
            #To avoid removing data from the profile we create a temp array using
            #the method list to avoid a linked copy
            temp_parents = list(new_prof.parents)
            #When not having access to a profile in geni, the parents provided are empty
            if prof_id in temp_parents : temp_parents.remove(prof_id)
            #Notice that we might have the situation of a single parent!
            if (len(temp_parents) > 0):
                #Let's find the profile which is already included.
                correct_parent = None
                if temp_parents[0] in children_matrix.keys(): correct_parent = temp_parents[0]
                else: correct_parent = temp_parents[1]
                children_matrix[correct_parent].append(new_prof)
                children_ids[correct_parent].append(new_prof.get_id())
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
                    gedcom_db.add_profile(prof_partner)
                    #And we mark is already in added profiles
                    self.added_profiles[id_partner] = prof_partner
                #We create here the family
                gedcom_db.add_family(father = init_profile.get_id(), mother = prof_partner.get_id(), children = children_ids[id_partner])