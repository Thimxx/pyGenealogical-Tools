from docutils.utils.math.latex2mathml import functions
__all__ = ["profile", "data_models", "immediate_family", "geniapi_common", "union", "geni2gedcom", "interface_geni_database"]

import requests, logging, re
from messages.pygeni_messages import ERROR_REQUESTS


#Several addresses of the Geni API
GENI_ADDRESS = "https://www.geni.com"
GENI_FAMILY = "/immediate-family"
GENI_INITIATE_PARAMETER = "?"
GENI_ADD_PARAMETER = "&"
GENI_TOKEN = "access_token="
GENI_SINGLE_TOKEN = GENI_INITIATE_PARAMETER + GENI_TOKEN
GENI_PARAM_TOKEN = GENI_ADD_PARAMETER + GENI_TOKEN
GENI_ADD_CHILD = "/add-child"
GENI_DELETE = "/delete"
GENI_ADD_PARTNER = "/add-partner"
GENI_UPDATE = "/update"
GENI_ADD_PARENT = "/add-parent"
#Parameters that depend on others
GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token" + GENI_SINGLE_TOKEN
GENI_API = GENI_ADDRESS + "/api/"
GENI_PEOPLE = GENI_ADDRESS + "/people/"
GENI_PROFILE =  GENI_API + "profile-"

GENI_CALLED_UNIONS = {}

#The token data
TOKEN = None

def get_token():
    '''
    Function to get the token value
    '''
    return TOKEN

def set_token(token_value):
    '''
    Function to set-up the token
    '''
    global TOKEN
    TOKEN = token_value

def update_geni_address(new_geni_address):
    '''
    This function will update the values of geni variables to be able to use
    in testing mode
    '''
    global GENI_ADDRESS
    global GENI_VALIDATE_TOKEN
    global GENI_API
    global GENI_PROFILE
    global GENI_SINGLE_TOKEN
    global GENI_PEOPLE
    #We update the variables
    GENI_ADDRESS = new_geni_address
    GENI_VALIDATE_TOKEN = GENI_ADDRESS + "/platform/oauth/validate_token" + GENI_SINGLE_TOKEN
    GENI_API = GENI_ADDRESS + "/api/"
    GENI_PEOPLE = GENI_ADDRESS + "/people/"
    GENI_PROFILE =  GENI_API + "profile-"
def geni_request_get(url):
    '''
    Function to perform get calls. Contains a loop in case there is a rate limit
    exceeded
    '''
    data = None
    continue_iteration = True
    i=1
    while continue_iteration:
        data = requests.get(url)
        i += 1
        #Common function for checking the consistency of delivered data
        continue_iteration = iteration_loop_logic(data)
    if "error" in data.json().keys():
        #Ok, now we know we have an error, we need to inform the user!
        logging.error(ERROR_REQUESTS + str(data.json()) + " in url " + url)
    return data
def geni_request_post(url, data_input = None):
    '''
    Function to perform post calls. Contains a loop in case there is a rate limit
    exceeded
    '''
    data = None
    if (data_input is None): data_input={}
    continue_iteration = True
    i=1
    while continue_iteration:
        data = requests.post(url, json=data_input)
        i += 1
        #Common function for checking the consistency of delivered data
        continue_iteration = iteration_loop_logic(data)
    if "error" in data.json().keys():
        #Ok, now we know we have an error, we need to inform the user!
        logging.error(ERROR_REQUESTS + str(data.json()))
    return data
def get_profile_id_from_address(prof_url):
    '''
    Function to extract the profile from the address
    '''
    return re.sub(r".*profile", "profile", prof_url)
def iteration_loop_logic(data):
    '''
    This piece of code is common between the post and the get methods inside functions
    above to connect to Geni, they have been separated for simplicity, it will check if there is any error
    in the obtained result
    data: output from he post or get methods
    output: True if the call shall continue and False if shall be stopped.
    '''
    value_error = data.json().get("error", {})
    if isinstance(value_error, dict):
        value_error = value_error.get("message", None)
    if not ( value_error and ("Rate limit exceeded." in value_error) ): return False
    return True