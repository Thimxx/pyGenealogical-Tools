import logging
from messages.parser_messages import *

class reader_input:
    '''
    General class parsing the data input
    '''
    def __init__(self, file_path):
        self.file = open(file_path, "r")

        self.profile = ""
        self.genikey = ""
        self.read_file()

        self.file.close()

    def read_file(self):
        '''
        Internal function reading the input file line by line
        '''
        self.continue_execution = True
        self.profile_given = False
        self.generations_given = False
        self.genikey_given = False
        self.climbancestors = False
        self.climbcousins = False
        for line in self.file:
            divided = line.split()
            if (divided[0] == "PROFILE"):
                self.profile = str(divided[1])
                self.profile_given = True
            elif (divided[0] == "GENIKEY"):
                self.genikey = str(divided[1])
                self.genikey_given = True
            elif (divided[0] == "CLIMB_ANCESTORS"):
                self.climbancestors = True
            elif (divided[0] == "CLIMB_COUSINS"):
                self.climbcousins = True
            elif (divided[0] == "GENERATIONS"):
                self.generations = int(divided[1])
                self.generations_given = True
        if (not self.genikey_given):
            logging.warning(GENI_KEY_MISSING)
            self.continue_execution = False
        if (self.climbancestors or self.climbcousins):
            if (not self.profile_given):
                logging.warning(PROFILE_MISSING)
                self.continue_execution = False
            if (not self.generations_given):
                logging.warning(GENERATIONS_MISSING)
                self.continue_execution = False