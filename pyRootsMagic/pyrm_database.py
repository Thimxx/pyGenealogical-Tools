'''
Created on 6 jul. 2019

@author: Val
'''
import sqlite3, logging
from datetime import datetime
from pyRootsMagic.rootsmagic_profile import rootsmagic_profile
from pyRootsMagic.rootsmagic_family import rootsmagic_family
from pyGenealogy.common_database import gen_database
from pyRootsMagic import collate_temp
from messages.py_rootsmagic_messages import WARNING_UPDATE_FAMILY_PARENTS

SEX_TO_DB = {"M" : "0", "F": "1", "U" : "2"}
LIVING_TO_DB = {True: "1", False: "0"}
EMPTY_VALUE = ""

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
    def get_potential_profile_match(self, profile, data_language = "en", name_convention = "father_surname"):
        '''
        This function will answer if profile might be already in the database
        and the id of the potential candidates
        profile shall be a derived class from pyGenealogy.common_profile
        '''
        potential_matches = []
        self.database.create_collation("RMNOCASE", collate_temp)
        profile_ids = "SELECT OwnerID FROM NameTable WHERE Surname LIKE ?"
        all_ids = self.database.execute(profile_ids, ( str(profile.getSurname()) , ) ).fetchall()
        #Now let's fetch the first value
        for id_prof in all_ids:
            new_prof = self.get_profile_by_ID(id_prof[0])
            score, factor = new_prof.comparison_score(profile, data_language, name_convention)
            if (score*factor > 2.0): potential_matches.append(id_prof[0])
        self.database.create_collation("RMNOCASE", None)
        return potential_matches
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
            
        new_name = ("INSERT INTO NameTable(OwnerID,Surname,Given,Prefix,Suffix,Nickname,NameType,Date,SortDate,IsPrimary,IsPrivate,Proof,EditDate,Sentence,"
                    "Note,BirthYear,DeathYear) VALUES(?,?,?,?,?,?,0,?,9223372036854775807,1,0,0,?,?,?,?,?)")
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
        
        father, mother shall be the RootsMagic id of the profile
        child should be an string of RootsMagic ID.
        marriage is an event from pyGenealogy.common_event
        '''
        child_id = "0"
        if children and (len(children) > 0): child_id = str(children[0])
        empty_value = ""
        new_family = ("INSERT INTO FamilyTable(FatherID, MotherID, ChildID, HusbOrder, WifeOrder, IsPrivate, Proof, SpouseLabel, FatherLabel,"
                      "MotherLabel, Note) VALUES(?,?,?,0,0,0,0,0,0,0,?)")
        cursor = self.database.cursor()
        cursor.execute( new_family, (str(father), str(mother), child_id, empty_value ) )
        family_id = cursor.lastrowid
        #If there are childrens declared we will also add to the family in one shot
        if children:
            self.add_child_to_family(family_id, children )
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
    def add_parents(self, child_profile_id = None, father_profile = None, mother_profile= None, marriage_event= None):
        '''
        This function will combine both add_profile and add_parent in a single creation
        child_profile_id shall be a rootsMagic ID (not the profile)
        father_profile and mother_profile shall be a inherited instance of pyGenealogy.common_profile
        marriage_event shall be an event of pyGenealogy.common_event class
        '''
        father_id = None
        mother_id = None
        #Firstly, both profiles of father and mother shall be created
        if father_profile: father_id = self.add_profile(father_profile)
        if mother_profile: mother_id = self.add_profile(mother_profile, spouseid = father_id)
        #Child shall be in the right format
        child_input = None
        if child_profile_id: child_input = [child_profile_id]
        #Once the parents are available, next step is to create the full family
        family_id = self.add_family(father = father_id, mother = mother_id, children = child_input, marriage = marriage_event)
        return father_id, mother_id, family_id
    def add_child_to_family(self, family_id, children ):
        '''
        Includes new children and updates the family with the new children
        family_id is the ide of the family to be added
        children is a list of id of childrens to be added
        '''
        #We need to add the parent in the profile description
        order = 0
        for child in children:
            #We need to update the child
            update_person = "UPDATE PersonTable SET ParentID = ? WHERE PersonID=?"
            self.database.execute( update_person, (family_id, str(child), ) )
            #We also need to update the child table
            create_child = ("INSERT INTO ChildTable(ChildID, FamilyID, RelFather, RelMother,ChildOrder, IsPrivate,"
                    "ProofFather, ProofMother,Note) VALUES(?,?,0,0,?,0,0,0,?)")
            self.database.execute( create_child, (str(child), family_id, str(order),EMPTY_VALUE, ) )
            order += 1
    def add_child(self, family_id, children_profiles ):
        '''
        It create a new child profile and adds to the family
        family_id shall be an id of the family
        children shall be an array of children profiles to be added
        '''
        child_ids = []
        for child_prof in children_profiles:
            id_child = self.add_profile(child_prof)
            child_ids.append(id_child)
        self.add_child_to_family(family_id, child_ids )
        return child_ids
    def add_partner(self, profile_id, partner_profile, marriage = None):
        '''
        Adds a partner to the profile, by firstly creating the partner and afterwards
        creating the family
        profile_id shall be the id of the profile
        partner_profile shall be the partner as a profile derivated by pyGenealogy.common_profile
        marriage shall be an instance of pyGenealogy.common_event
        '''
        id_partner = self.add_profile(partner_profile)
        id_family = None
        if partner_profile.getGender() == "M":
            id_family = self.add_family(father = id_partner, mother = profile_id, marriage = marriage)
        else:
            id_family = self.add_family(father = profile_id, mother = id_partner, marriage = marriage)
        return id_partner, id_family
#===============================================================================
#         UPDATE methods: all methods compatible with common_database
#===============================================================================
    def update_family(self, family_id, father_id = None, mother_id = None, children = None, marriage = None):
        '''
        Updates an existing family with new data
        
        father, mother shall be the RootsMagic id of the profile, as a minimum one of the profiles shall be already in the family
        child should be an string of RootsMagic IDs.
        marriage is an event from pyGenealogy.common_event
        '''
        if not (father_id or mother_id):
            logging.warning(WARNING_UPDATE_FAMILY_PARENTS)
            return None
        if father_id:
            update_family = "UPDATE FamilyTable SET FatherID=? WHERE FamilyID=?"
            self.database.execute( update_family, (father_id, family_id, ) )
            #As we add teh family, we shall update also the person
            update_person = "UPDATE PersonTable SET SpouseID = ? WHERE PersonID=?"
            self.database.execute( update_person, (family_id, father_id, ) )
            if marriage:
                father = self.get_profile_by_ID(father_id)
                father.setNewMarriage(marriage, family_id)
        if mother_id:
            update_family = "UPDATE FamilyTable SET MotherID=? WHERE FamilyID=?"
            self.database.execute( update_family, (mother_id, family_id, ) )
            #As we add teh family, we shall update also the person
            update_person = "UPDATE PersonTable SET SpouseID = ? WHERE PersonID=?"
            self.database.execute( update_person, (family_id, mother_id, ) )
            if marriage:
                mother = self.get_profile_by_ID(mother_id)
                mother.setNewMarriage(marriage, family_id)
        if children:
            self.add_child_to_family(family_id, children)
        self.database.commit()