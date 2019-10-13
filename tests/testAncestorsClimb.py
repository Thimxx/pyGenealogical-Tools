'''
Created on 8 ago. 2017

@author: Val
'''
import unittest
import os
from pyGeni import set_token
from pyGeni.profile import profile
from tests.FIXTURES import PHILIPIVg, FLAVIAg, COUSIN_PROFILE
from analyzefamily.ancerstors_climb import climb
from pyGeni.interface_geni_database import geni_database_interface
from pyRootsMagic.pyrm_database import database_rm

class testAncestorsClimb(unittest.TestCase):

    def setUp(self):
        set_token(os.environ['GENI_KEY'])
        #This is used to identify the locationo of the file
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2
 
    def testCountingOfAncestors(self):
        '''
        Testing the right calculation of ancestors. We know Philip IV was
        having duplicated ancestors, so the number will be lower than the 
        generation count.
        '''
        #Database creation
        geni_db = geni_database_interface()
        philip = profile(PHILIPIVg)
        
        climber = climb(geni_db)
        
        ancest = climber.get_ancestors(philip, 4)
        assert(len(ancest[1].keys()) == 23)
        
    def testStopWithNoAncestors(self):
        '''
        If there are no longer ancestors, the ancestor climb should stop.
        Checking if that works! This profile has only one generation available
        '''
        #Database creation
        geni_db = geni_database_interface()
        flavia = profile(FLAVIAg)
        
        climber = climb(geni_db)
        
        ancestors = climber.get_ancestors(flavia, 6)
        assert(len(ancestors[1].keys())  == 3)
    
    def testCousinsExecution(self):
        '''
        We will test the cousins execution in different way. Will be tested by
        number, not by person
        '''
        #Database creation
        geni_db = geni_database_interface()
        philip = profile(COUSIN_PROFILE)
        generations = 2
        
        climber = climb(geni_db)
        ancestors, anc_count, profiles = climber.get_cousins(philip, generations)
        
        total_center = 0
        total_outside = 0
        for i in range(0, generations+1):
            total_center = total_center + anc_count[i][i]
            for j in range(i+1, generations + 1):
                total_outside = total_outside + anc_count[i][j]
        assert(total_center == 7) 
        assert(total_outside == 0) 
        
        total_final = 0
        for i in range(0, generations+1):
            for j in range(0, generations + 1):
                total_final = total_final + anc_count[i][j]
        assert(total_final == 36)
        assert(len(profiles) == 36)
    
    def test_using_roots_magic(self):
        '''
        Test using climber with RootsMagic database
        '''
        file_rm = os.path.join(self.filelocation, "Rootstest.rmgc")
        rm_db = database_rm(file_rm)
        #We create the climber with the RM database
        climber = climb(rm_db)
        prof = rm_db.get_profile_by_ID(1)
        #We execute the ancestors
        ancestors, data_gen = climber.get_ancestors(prof, 4)
        i = 0
        for generation in ancestors:
            i = i + len(generation)
        assert(i == 7)
        total = 0
        for id_value in data_gen.values():
            total += id_value
        assert(total == 3.0)
        
        cousins, cousins_count, profiles_score = climber.get_cousins(prof, 2)
        assert(cousins[2][2] == [4,5,8])
        assert(cousins_count[2][1] == 1)
        assert(sum(list(profiles_score.values())) == 3.5)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()