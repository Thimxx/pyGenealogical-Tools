'''
Created on 15 ago. 2017

@author: Val
'''

from openpyxl import load_workbook

class getFSfamily(object):
    '''
    This class reads the  FS output excel from the website of FamilySearch
    '''


    def __init__(self, filename):
        '''
        This contructor reads the output file from FS in xlsx format
        '''
        self.loaded_data = load_workbook(filename)
        