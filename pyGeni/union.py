'''
Created on 19 sept. 2017

@author: Val
'''

import pyGeni as geni
from pyGeni.geniapi_common import geni_calls
from datetime import date

class union(geni_calls):
    '''
    This class will be extracting data about unions in Geni
    '''
    def __init__(self, union_id):
        '''
        Constructor it takes the union id from Geni
        '''
        #We initiate the base classes
        geni_calls.__init__(self)
        url = geni.GENI_API + union_id + geni.GENI_SINGLE_TOKEN + geni.get_token()
        r = geni.geni_request_get(url)
        data = r.json()
        self.union_data = {}
        for key_value in data.keys():
            if key_value == "id": self.union_data["id"] = data[key_value]
            if key_value == "url": self.union_data["url"] = data[key_value]
            if key_value == "guid": self.union_data["guid"] = data[key_value]
            if key_value == "marriage_date":
                day = data["marriage_date"].get("day", 1)
                month = data["marriage_date"].get("month", 1)
                year = data["marriage_date"].get("year", 1)
                self.union_data["marriage_date"] = date(year, month, day)
            if key_value == "marriage_location":
                self.union_data["marriage_place"] = {}
                for location_key in data["marriage_location"].keys():
                    if location_key == "city": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "county": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "state": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "country": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "country_code": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "latitude": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "longitude": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
                    if location_key == "formatted_location": self.union_data["marriage_place"][location_key] = data["marriage_location"][location_key]
            if key_value == "status": self.union_data["status"] = data[key_value]
            if key_value == "partners": self.union_data["partners"] = data[key_value]
            if key_value == "children": self.union_data["children"] = data[key_value]
            