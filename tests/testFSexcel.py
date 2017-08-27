'''
Created on 15 ago. 2017

@author: Val
'''
import unittest
from pyFS.pyfs_open_xlsx import getFSfamily
import os
import datetime

class Test(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        location1 = os.path.join(os.getcwd(), "fixtures_files")
        location2 = os.path.join(os.getcwd(), "tests", "fixtures_files")
        if os.path.exists(location1):
            self.filelocation = location1
        else:
            self.filelocation = location2



    def test_fs_reader(self):
        '''
        Test reading an input file
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado.xlsx")
        fsclass = getFSfamily(input_file)
        assert(fsclass.correct_execution)
        assert(fsclass.initial_column == "A")
        assert(fsclass.initial_row == 6)
        assert(fsclass.sheet_title == "Sheet0")
    
    def test_wrong_inputs(self):
        '''
        Test FS reader wrong inputs are detected
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado.xlsx")
        fsclass = getFSfamily(input_file, naming_convention = "wrong_input")
        self.assertFalse(fsclass.correct_execution)
        
    
    def test_fs_reader_single_person(self):
        '''
        Tests in detail the correct reading of a person
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado-singleperson.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname")
        this_profile = fsclass.profiles[0]
        
        assert(fsclass.correct_execution)
        assert (len(fsclass.profiles) == 1)
        assert(this_profile.gender == "M")
        assert(this_profile.name == "Wenceslao")
        assert(this_profile.surname == "Potente Asegurado")
        assert(this_profile.birth_date == datetime.date(1862,9,28))
        assert(this_profile.accuracy_birth_date == "EXACT")
        assert(this_profile.baptism_date == datetime.date(1862,10,2))
        assert(this_profile.accuracy_baptism_date == "EXACT")
        assert(this_profile.residence_date == datetime.date(1862,1,1))
        assert(this_profile.accuracy_residence_date == "ABOUT")
        assert(this_profile.death_date == datetime.date(1863,6,28))
        assert(this_profile.accuracy_death_date == "EXACT")
        assert(this_profile.burial_date == datetime.date(1863,6,28))
        assert(this_profile.accuracy_burial_date == "EXACT")
        assert(this_profile.death_place == ['La Parrilla', 'Valladolid', 'Spain'])
        assert(this_profile.residence_place == ['La Parrilla', 'Valladolid', 'Spain'])
        assert(this_profile.baptism_place == ['Nuestra Señora de los Remedios', 'La Parrilla', 'Valladolid', 'Spain'])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fs_reader']
    unittest.main()