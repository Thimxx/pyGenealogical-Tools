'''
Created on 6 jul. 2019

@author: Val
'''
import sqlite3
from datetime import datetime
from pyRootsMagic.rootsmagic_profile import rootsmagic_profile
from pyRootsMagic.rootsmagic_family import rootsmagic_family
from pyGenealogy.common_database import gen_database
from pyRootsMagic import collate_temp

SEX_TO_DB = {"M" : "0", "F": "1", "U" : "2"}
LIVING_TO_DB = {True: "1", False: "0"}

class database_rm(gen_database):
    '''
    This class is used for reading a database RootsMagic and allowing to access
    to the different profiles.
    '''
    def __init__(self, db_file):
        '''
        Construction, taking as initial parameter the location of the database
        '''
        gen_database.__init__(self)
        self.database = None
        self.right_read = False
        #Open database and get it as part of the class
        self.database = sqlite3.connect(db_file)
    def close_db(self):
        '''
        Closes the database
        '''
        self.database.close()
#===============================================================================
#         GET methods: all methods compatible with common_database
#===============================================================================
    def get_db_kind(self):
        '''
        Identified of the kind of database in use
        '''
        return "ROOTSMAGIC"
    def get_profile_by_ID(self, id_profile):
        '''
        Returns the profile by the input ID
        '''
        profile_id = "SELECT * FROM PersonTable WHERE PersonID=?"
        profile_cursor = self.database.execute(profile_id, (str(id_profile),) )
        #Now let's fetch the first value
        is_profile_in = profile_cursor.fetchone()
        if is_profile_in:
            return rootsmagic_profile(id_profile, self.database)
        else:
            return None
    def get_family_by_ID(self, id_family):
        '''
        Returns the profile by the input ID
        '''
        family_id = "SELECT * FROM FamilyTable WHERE FamilyID=?"
        family_cursor = self.database.execute(family_id, (str(id_family),) )
        #Now let's fetch the first value
        is_family_in = family_cursor.fetchone()
        if is_family_in:
            return rootsmagic_family(id_family, self.database)
        else:
            return None
    def get_all_profiles(self):
        '''
        Returns all profiles in the database
        '''
        res_names = self.database.execute("SELECT * FROM PersonTable")
        #We obtain now all profiles
        profiles = {}
        for name in res_names:
            prof = rootsmagic_profile(name[0], self.database)
            profiles[name[0]] = prof
        return profiles.values()
    def get_family_from_child(self, profile_id):
        '''
        It will return the family of a profile where is the child
        Returns the id of the family and the family object
        '''
        family_id = "SELECT * FROM ChildTable WHERE ChildID=?"
        family_cursor = self.database.execute(family_id, (str(profile_id),) )
        #Now let's fetch the first value, we are not expecting several fathers
        is_family_in = family_cursor.fetchone()
        if is_family_in:
            return int(is_family_in[2]), self.get_family_by_ID(is_family_in[2])
        else:
            return None, None
    def get_all_family_ids_is_parent(self, profile_id):
        '''
        It will provide all the families where the profile is one of the parents
        '''
        families = []
        family_id = "SELECT * FROM FamilyTable WHERE FatherID=? OR MotherID=?" 
        family_cursor = self.database.execute(family_id, (str(profile_id),str(profile_id),) )
        #There can be several families
        for family in family_cursor:
            families.append(int(family[0]))
        return families
    def get_all_children(self, profile_id):
        '''
        This function will provide all the children associated to a profile
        '''
        children = []
        #First, we get all families
        families = self.get_all_family_ids_is_parent(profile_id)
        for family_id in families:
            child_db = "SELECT * FROM ChildTable WHERE FamilyID=?"
            child_cursor = self.database.execute(child_db, (str(family_id),) )
            for child in child_cursor:
                children.append(child[1])
        return children
#===============================================================================
#         ADD methods: Add methods used to include a new profile and new family
#===============================================================================
    def add_profile(self, profile, parentid = 0, spouseid = 0):
        '''
        It will add a new profile in the database
        '''
        edit_date_value = str( (datetime.today()- datetime(1899,12,31) ).days)
        empty_value=""
        #Adding the Person before the name
        new_person = ("INSERT INTO PersonTable (Sex, EditDate, ParentID, SpouseID, Color, Relate1, Relate2, Flags, Living, IsPrivate,Proof,Bookmark,Note)"
                    " VALUES(?,?,?,?,0,0,0,0,?,0,0,0,?)")
        cursor = self.database.cursor()
        cursor.execute(new_person, (SEX_TO_DB[profile.getGender()], edit_date_value, str(parentid), str(spouseid),
                                  LIVING_TO_DB[profile.getLiving()], empty_value,
                                   ) )
        row_data = cursor.lastrowid
        #Adding the Name once known the Person
        birth_year = "0"
        death_year = "0"
        birth_event = profile.get_specific_event("birth")
        death_event = profile.get_specific_event("death")
        if (birth_event and birth_event.get_year()) : birth_year = birth_event.get_year()
        if (death_event and death_event.get_year()) : death_year = death_event.get_year()
        self.database.create_collation("RMNOCASE", collate_temp)
            
        new_name = ("INSERT INTO NameTable(OwnerID,Surname,Given,Prefix,Suffix,Nickname,NameType,Date,SortDate,IsPrimary,IsPrivate,Proof,EditDate,Sentence,Note,BirthYear,DeathYear)"
                    " VALUES(?,?,?,?,?,?,0,?,9223372036854775807,1,0,0,?,?,?,?,?)")
        self.database.execute( new_name, (str(row_data), profile.getSurname(), profile.getName(),empty_value, empty_value,
                                empty_value, ".", "0.0",empty_value,empty_value,birth_year,death_year,
                                ) )
        added_profile = self.get_profile_by_ID(row_data)
        for event in profile.getEvents():
            added_profile.setNewEvent(event)
        
        self.database.create_collation("RMNOCASE", None)
        
        self.database.commit()
        return row_data
    def add_family(self, father = "0", mother = "0", children = None, marriage = None):
        '''
        Includes a new family inside rootsmagic_family
        
        father, mother the RootsMagic id of them
        child should be an string of get_child
        marriage is an event
        '''
        child_id = "0"
        if children and (len(children) > 0): child_id = str(children[0])
        empty_value = ""
        new_family = "INSERT INTO FamilyTable(FatherID, MotherID, ChildID, HusbOrder, WifeOrder, IsPrivate, Proof, SpouseLabel, FatherLabel,MotherLabel, Note) VALUES(?,?,?,0,0,0,0,0,0,0,?)"
        cursor = self.database.cursor()
        cursor.execute( new_family, (str(father), str(mother), child_id, empty_value ) )
        family_id = cursor.lastrowid
        
        if children:
            #We need to add the parent in the profile description
            order = 0
            for child in children:
                #We need to update the child
                update_person = "UPDATE PersonTable SET ParentID = ? WHERE PersonID=?"
                self.database.execute( update_person, (family_id, str(child), ) )
                #We also need to update the child table
                create_child = "INSERT INTO ChildTable(ChildID, FamilyID, RelFather, RelMother,ChildOrder, IsPrivate,ProofFather, ProofMother,Note) VALUES(?,?,0,0,?,0,0,0,?)"
                self.database.execute( create_child, (str(child), family_id, str(order),empty_value, ) )
                order += 1
        update_persons = []
        if father != 0: update_persons.append(father)
        if mother != 0: update_persons.append(mother)
        for parent_add in update_persons:
            update_person = "UPDATE PersonTable SET SpouseID = ? WHERE PersonID=?"
            self.database.execute( update_person, (family_id, str(parent_add), ) )
        self.database.commit()
        if marriage:
            prof = None
            if father != 0: prof = self.get_profile_by_ID(father)
            if mother != 0: prof = self.get_profile_by_ID(mother)
            prof.setNewMarriage(marriage, family_id)
        return family_id