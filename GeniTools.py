from pyGeni import profile
from parser_input import reader_input
from analyzefamily.ancerstors_climb import climb
from messages.genitools_messages import *
import logging



def main():
    logging.basicConfig(filename='GeniToools.log', level=logging.INFO)
    logging.info('Starting GeniTools\n' + "="*20 +"\n")
    
    #Firstly the Input File is Read
    data = reader_input.reader_input("INPUT")
    
    if (data.continue_execution):
        #We only continue if inputs are correct!
        test_profile = profile.profile(data.profile, data.genikey)

        if (data.climbancestors or data.climbcousins):
            climber = climb(test_profile)
            if (data.climbcousins):
                ancestors, matrix_count, included_profiles = climber.get_cousins(data.generations)
                print(matrix_count)
            if (data.climbancestors):
                ancestors, affected_profiles = climber.get_ancestors(data.generations)
    else:
        logging.error(ERROR_MISSING_DATA)

    logging.info('Finishing GeniTools' + "="*20 +"\n")

if __name__ == '__main__':
    main()



