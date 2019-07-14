'''
Created on 8 ago. 2017

@author: Val
'''

import pyGeni as s
from pyGeni.geniapi_common import geni_calls
from pyGeni.data_models import geni_union
from pyGeni.union import union

class immediate_family(geni_calls):
    '''
    This function is used to call the immediate family api from Geni.
    '''
    def __init__(self, myid):
        '''
        The constructor will also make the call to the web to get the right
        string
        '''
        #Initiating base class
        geni_calls.__init__(self)
        self.union_url = self.get_profile_url(myid) + s.GENI_FAMILY + self.token_string()
        r = s.geni_request_get(self.union_url)
        self.data = r.json()
        #we initialize the lists
        self.union_extracted = False
        self.parents = []
        self.sibligns = []
        self.partner = []
        self.children = []
        self.parent_union = []
        self.marriage_union = []
        self.marriage_events = []
        if not( 'error' in self.data ):
            #In this case, we have extracted properly the union data
            self.union_extracted = True
            #the nodes include the data of the different affected profiles and unions
            for keydata in self.data["nodes"].keys():
                #is easier to go to the usions, so we filter by unions.
                if "union" in keydata:
                    #Good... let's obtain the data from the union
                    tmp_union = geni_union(self.data["nodes"][keydata], keydata)
                    #Now we need to filter the parents and children as we should not duplicate
                    if tmp_union.is_profile_child(myid):
                        #We know is a child... so
                        self.parents = self.parents + tmp_union.parents
                        tmp_union.children.remove(myid)
                        self.sibligns = self.sibligns + tmp_union.children
                        self.parent_union.append(tmp_union)
                    else:
                        #In this case we know is a marriage union
                        tmp_union.parents.remove(myid)
                        self.partner = self.partner +  tmp_union.parents
                        self.children = self.children + tmp_union.children
                        #We obtain the union from Geni in order to introduce the marriage
                        marriage_union = union(tmp_union.union_id)
                        self.marriage_union.append(tmp_union)
                        if "marriage" in marriage_union.union_data.keys():
                            self.marriage_events.append( marriage_union.union_data.get('marriage', None))