'''
Created on 6 July 2019

@author: Val
'''
__all__ = ["pyrm_database", "rootsmagic_family", "rootsmagic_profile", "collate_temp"]


def collate_temp(string1, string2):
    '''
    This is a fake function used to solve the problem of the RMNOCASE issue inside the database
    '''
    if string1 == string2:
        return 0
    elif string1 > string2:
        return 1
    else:
        return -1