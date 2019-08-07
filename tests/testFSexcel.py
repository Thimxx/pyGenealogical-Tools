'''
Created on 15 ago. 2017

@author: Val
'''
import unittest
from pyFS.pyfs_open_xlsx import getFSfamily
import os
from pyGeni import profile
import datetime

class Test(unittest.TestCase):
    def setUp(self):
        '''
        Let's make it simple... is just a test not a good code. If it is not located in one place will
        be in another!
        '''
        #We used the sandbox here
        profile.s.set_token(os.environ['GENI_KEY'])
        profile.s.update_geni_address("https://www.sandbox.geni.com")
        #profile.s.VERIFY_INPUT = False
        #We locate the folder here
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
        fsclass = getFSfamily(input_file, naming_convention="spanish_surname", language="es")
        assert(fsclass.correct_execution)
        assert(fsclass.initial_column == 1)
        assert(fsclass.initial_row == 6)
        assert(fsclass.sheet_title == "Sheet0")

        #Maria Potente Asegurado
        assert(fsclass.profiles[0].gen_data["birth"].get_date() == datetime.date(1853,9,8))
        assert(fsclass.profiles[0].gen_data["baptism"].get_date() == datetime.date(1853,9,13))
        assert(fsclass.profiles[0].gen_data["burial"].get_date() == datetime.date(1853,9,30))
        assert(fsclass.profiles[0].gen_data["baptism"].get_location()["city"] == "La Parrilla")
        assert(fsclass.profiles[0].gen_data["death"].get_location()["place_name"] == "La Parrilla")
        assert(len(fsclass.profiles[0].gen_data["web_ref"]) == 3)
        assert(fsclass.profiles[0].gen_data["residence"].get_year() == 1853)
        assert(fsclass.profiles[0].gen_data["residence"].get_accuracy() == "ABOUT")
        #Wenceslao Potente Asegurado
        assert(fsclass.profiles[2].gen_data["birth"].get_date() == datetime.date(1862,9,28))
        assert(fsclass.profiles[2].gen_data["baptism"].get_date() == datetime.date(1862,10,2))
        assert(fsclass.profiles[2].gen_data["death"].get_date() == datetime.date(1863,6,28))
        assert(fsclass.profiles[2].gen_data["burial"].get_date() == datetime.date(1863,6,28))
        assert(fsclass.profiles[2].gen_data["baptism"].get_location()["city"] == "La Parrilla")
        assert(fsclass.profiles[2].gen_data["death"].get_location()["place_name"] == "La Parrilla")
        assert(len(fsclass.profiles[2].gen_data["web_ref"]) == 2)
        assert(fsclass.profiles[2].gen_data["residence"].get_year() == 1862)
        #Evarista Potente Asegurado
        assert(fsclass.profiles[4].gen_data["birth"].get_date() == datetime.date(1857,10,26))
        assert(fsclass.profiles[4].gen_data["baptism"].get_date() == datetime.date(1857,11,1))
        assert(fsclass.profiles[4].gen_data["burial"].get_date() == datetime.date(1858,2,25))
        assert(fsclass.profiles[4].gen_data["baptism"].get_location()["city"] == "La Parrilla")
        assert(fsclass.profiles[4].gen_data["death"].get_location()["place_name"] == "La Parrilla")
        assert(len(fsclass.profiles[4].gen_data["web_ref"]) == 2)
        assert(fsclass.profiles[4].gen_data["residence"].get_year() == 1857)


    def test_wrong_inputs(self):
        '''
        Test FS reader wrong inputs are detected
        '''
        input_file = os.path.join(self.filelocation, "fs-PotenteAsegurado.xlsx")
        fsclass = getFSfamily(input_file, naming_convention = "wrong_input")
        self.assertFalse(fsclass.correct_execution)
        self.assertFalse(fsclass.create_profiles_in_Geni("data"))
        self.assertFalse(fsclass.create_gedcom_file("myoutput"))

    def test_empty_excel(self):
        '''
        Test an empty excel from FS
        '''
        input_file = os.path.join(self.filelocation, "fs-Empty.xlsx")
        fsclass = getFSfamily(input_file)
        self.assertFalse(fsclass.correct_execution)

    def test_issue_double_names(self):
        '''
        Test composed names
        '''
        input_file = os.path.join(self.filelocation, "fs-MolpecerezGomez.xls")
        fsclass = getFSfamily(input_file, naming_convention = "spanish_surname")
        for profile in fsclass.profiles:
            assert(profile.gen_data["name"] in ["Eusebio", "Petra", "Román", "Gila", "Segunda", "Julián", "Petra Regalada"])
        os.remove(os.path.join(self.filelocation, "fs-MolpecerezGomez.xlsx"))

        file_ged = os.path.join(self.filelocation, "fs-MolpecerezGomez.ged")
        if os.path.exists(file_ged): os.remove(file_ged)
        #This one will create the gedcomfile
        fsclass.create_gedcom_file(file_ged)
        assert(os.path.exists(file_ged))
        if os.path.exists(file_ged): os.remove(file_ged)
    def test_not_existing_file(self):
        '''
        Test file not existing
        '''
        input_file = os.path.join(self.filelocation, "fs-DOESNOTEXIST.xls")
        fsclass = getFSfamily(input_file, naming_convention = "spanish_surname")
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
        assert(this_profile.gen_data["birth"].get_date() == datetime.date(1862,9,28))
        assert(this_profile.gen_data["birth"].get_accuracy() == "EXACT")
        assert(this_profile.gen_data["baptism"].get_date() == datetime.date(1862,10,2))
        assert(this_profile.gen_data["baptism"].get_accuracy() == "EXACT")
        assert(this_profile.gen_data["residence"].year == 1862)
        assert(this_profile.gen_data["residence"].get_accuracy() == "ABOUT")
        assert(this_profile.gen_data["death"].get_date() == datetime.date(1863,6,28))
        assert(this_profile.gen_data["death"].get_accuracy() == "EXACT")
        assert(this_profile.gen_data["burial"].get_date() == datetime.date(1863,6,28))
        assert(this_profile.gen_data["burial"].get_accuracy() == "EXACT")
        assert(this_profile.gen_data["death"].get_location()["place_name"] == 'La Parrilla')
        assert(this_profile.gen_data["birth"].get_location()["place_name"] == 'La Parrilla')
        assert(this_profile.gen_data["baptism"].get_location()["place_name"] == 'Calle Nuestra Señora De Los Remedios')
        assert(len(this_profile.gen_data["nicknames"]))
        assert("Wenceslao Potente" in this_profile.gen_data["nicknames"])

    def test_name_with_particle(self):
        '''
        Test bug of names with particle
        '''
        input_file = os.path.join(self.filelocation, "fs-CaballeroBargas.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")

        juan_in = False

        for prof in fsclass.profiles:
            if ("juan de" in prof.gen_data["name"].lower()): juan_in = True

        self.assertFalse(juan_in)

    def test_bug_not_identifying_surname_of_partner(self):
        '''
        Test missing surname of partner
        '''
        input_file = os.path.join(self.filelocation, "fs-ZamoraEsteban.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")
        assert(fsclass.related_profiles[0].gen_data["surname"] == "Recio de Diego")
        assert(fsclass.related_profiles[1].gen_data["surname"] == "Toral Martín")
        assert(fsclass.parents_profiles[0][0].gen_data["surname"] =="Recio")
        assert(fsclass.parents_profiles[0][1].gen_data["surname"] =="de Diego")
        assert(fsclass.parents_profiles[1][0].gen_data["surname"] =="Toral")
        assert(fsclass.parents_profiles[1][1].gen_data["surname"] =="Martín")

    def test_bug_equal_surnames(self):
        '''
        Test parents with same surname not captured
        '''
        input_file = os.path.join(self.filelocation, "fs-NuñezArribas.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")
        for prof in fsclass.related_profiles:
            assert(fsclass.related_profiles[prof].gen_data["surname"] == "Sanz Sanz")


    def test_binfo(self):
        '''
        Test missing surname of partner
        '''
        input_file = os.path.join(self.filelocation, "fs-ArribasRuiz.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")
        for prof in fsclass.profiles:
            assert(prof.gen_data["surname"] == "Arribas Ruiz")


    def test_issue_double_surname_mother_partner(self):
        '''
        Test securing right surname transferred for mother of partner
        '''
        input_file = os.path.join(self.filelocation, "fs-MartinFernandez.xlsx")
        fsclass = getFSfamily(input_file, "spanish_surname", language = "es")
        assert(fsclass.related_profiles[3].gen_data["surname"] == "de Ayala Martínez")
    
    def test_issue_single_parent(self):
        '''
        Test no issue with a single parent in marriage
        '''
        #No need to check anything, just making sure it works ok.
        input_file = os.path.join(self.filelocation, "fs-JuarezRuiz.xlsx")
        getFSfamily(input_file, "spanish_surname", language = "es")
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_fs_reader']
    unittest.main()
