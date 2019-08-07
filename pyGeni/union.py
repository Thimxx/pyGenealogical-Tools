'''
Created on 19 sept. 2017

@author: Val
'''

import pyGeni as geni
from pyGeni.geniapi_common import geni_calls
from pyGenealogy.common_event import event_profile
from pyGenealogy.common_family import family_profile

class union(geni_calls, family_profile):
    '''
    This class will be extracting data about unions in Geni
    '''
    def __init__(self, union_id):
        '''
        Constructor it takes the union id from Geni
        '''
        #We initiate the base classes
        geni_calls.__init__(self)
        family_profile.__init__(self)
        data = ""
        if (union_id in geni.GENI_CALLED_UNIONS):
            #In order to save calls we try to save the different calls
            data = geni.GENI_CALLED_UNIONS[union_id]
        else:
            url = geni.GENI_API + union_id + geni.GENI_SINGLE_TOKEN + geni.get_token()
            r = geni.geni_request_get(url)
            data = r.json()
            geni.GENI_CALLED_UNIONS[union_id] = data
        self.union_data = {}
        for key_value in data.keys():
            if key_value == "id": self.union_data["id"] = data[key_value]
            if key_value == "url": self.union_data["url"] = data[key_value]
            if key_value == "guid": self.union_data["guid"] = data[key_value]
            if key_value == "marriage_date":
                #We might have an existing marriage in the file
                    self.union_data["marriage"] = self.get_date("marriage", data["marriage_date"], previous_event = self.union_data.get("marriage", None))
            if key_value == "marriage_location":
                place_data = {}
                for location_key in data["marriage_location"].keys():
                    if location_key == "city": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "county": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "state": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "country": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "country_code": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "latitude": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "longitude": place_data[location_key] = data["marriage_location"][location_key]
                    if location_key == "formatted_location": place_data[location_key] = data["marriage_location"][location_key]
                if not ("marriage" in self.union_data.keys()): self.union_data["marriage"] = event_profile("marriage")
                self.union_data["marriage"].setLocationAlreadyProcessed(place_data)
            if key_value == "status": self.union_data["status"] = data[key_value]
            if key_value == "partners":
                self.union_data["partners"] = data[key_value]
                self.setFather(geni.get_profile_id_from_address(data[key_value][0]))
                if len(data.get(key_value, None)) > 1: self.setMother(geni.get_profile_id_from_address(data[key_value][1]))
            if key_value == "children":
                self.union_data["children"] = data[key_value]
                children = []
                for child in data[key_value]:
                    children.append(geni.get_profile_id_from_address(child))
                self.setChild(children)