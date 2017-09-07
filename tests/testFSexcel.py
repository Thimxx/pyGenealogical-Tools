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
    
    def test_fs_with_a_marriage(self):
        '''
        Test a FS file with marriage
        '''
        input_file = os.path.join(self.filelocation, "fs-MartinPerez.xlsx")
        fsclass = getFSfamily(input_file)
        assert(fsclass.correct_execution)
        first_profile = fsclass.profiles[0]
        print()
        assert(first_profile.gen_data["name"] == "Tiburcio")
        second_profile = fsclass.profiles[1]
        assert(second_profile.gen_data["name"] == "Lucia")
        married_profile = fsclass.profiles[2]
        assert(married_profile.gen_data["name"] == "Nicasia")
        assert(married_profile.gen_data["marriage_place"]["city"] == "Tudela de Duero")
    
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
        assert(this_profile.gen_data["gender"] == "M")
        assert(this_profile.gen_data["name"] == "Wenceslao")
        assert(this_profile.gen_data["surname"] == "Potente Asegurado")
        assert(this_profile.gen_data["birth_date"] == datetime.date(1862,9,28))
        assert(this_profile.gen_data["accuracy_birth_date"] == "EXACT")
        assert(this_profile.gen_data["baptism_date"] == datetime.date(1862,10,2))
        assert(this_profile.gen_data["accuracy_baptism_date"] == "EXACT")
        assert(this_profile.gen_data["residence_date"] == datetime.date(1862,1,1))
        assert(this_profile.gen_data["accuracy_residence_date"] == "ABOUT")
        assert(this_profile.gen_data["death_date"] == datetime.date(1863,6,28))
        assert(this_profile.gen_data["accuracy_death_date"] == "EXACT")
        assert(this_profile.gen_data["burial_date"] == datetime.date(1863,6,28))
        assert(this_profile.gen_data["accuracy_burial_date"] == "EXACT")
        assert(this_profile.gen_data["death_place"]["city"] == 'La Parrilla')
        assert(this_profile.gen_data["residence_place"]["state"] == 'Castile and León')
        assert(this_profile.gen_data["baptism_place"]["place_name"] == 'Nuestra Señora de los Remedios')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fs_reader']
    unittest.main()