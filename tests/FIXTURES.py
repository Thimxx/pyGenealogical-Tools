#Testing fixtures for unions

#Philip IV of Spain
PHILIPIVg = "6000000000837888160"
PHILIPIVid = "profile-4197014"
PHILIPIVget = "4197014"

#Flavia Maxima Theodora
#https://www.geni.com/people/Flavia-Maximiana-Theodora/6000000012560069447
FLAVIAg = "6000000012560069447"

#Example of union from Geni
UNION_EXAMPLE = {'url': 'https://www.geni.com/api/union-8823523', 'status': 'spouse', 'edges': {'profile-4197014': {'rel': 'partner'}, 'profile-3561190': {'rel': 'partner'}, 'profile-99981031': {'rel': 'child'}, 'profile-99981066': {'rel': 'child'}, 'profile-99981097': {'rel': 'child'}, 'profile-99981131': {'rel': 'child'}, 'profile-4197318': {'rel': 'child'}, 'profile-117291254': {'rel': 'child'}, 'profile-44032552': {'rel': 'child'}, 'profile-3561371': {'rel': 'child'}, 'profile-34684951598': {'rel': 'child'}}}
UNION_EXAMPLE_ID = "union-8823523"
UNION_EXAMPLE_PARENT = "profile-4197014"
UNION_EXAMPLE_CHILD  = "profile-99981031"
UNION_EXAMPLE_NOT_INCLUDED = "profile-00000000"
UNION_EXAMPLE_NUMBER_CHILDREN = 9
UNION_MARRIAGE = "https://www.geni.com/api/union-8813338"
UNION_SANDBOX = "union-155"

#Cousing test, using a profile with smaller documented relatives!
COUSIN_PROFILE = "6000000014013164881"

#Small example of a Geni_KEY
GENI_KEY_EXAMPLE = "fasjkgsdfsnnk44534078262"


#Living place
GENERIC_PLACE_STRING = "Arrabal de Portillo,Valladolid,Spain"
GENERIC_PLACE_WITH_PLACE = "Nuestra Señora de los Remedios, La Parrilla, Valladolid, Spain" 
GENERIC_PLACE_IN_DICTIONARY = {'raw': 'Portillo,Valladolid,Castile and Leon,Spain', 'city': 'Portillo', 'county': 'Valladolid', 'state': 'Castilla y León', 'country': 'Spain', 'latitude': 41.47815569999999, 'longitude': -4.5863041}
GENERIC_PLACE_CAPITALS = "SAN JUAN EVANGELISTA DEL ARRABAL,ARRABAL DE PORTILLO,VALLADOLID,SPAIN"
#Year Examples
RIGHT_YEAR = "1894"
RIGHT_YEAR_IN_A_TEXT = "This year is 1894"
RIGHT_YEAR_IN_A_DATE = "14 Aug 1894"
WRONG_YEAR = "3845"
JUST_TEXT = "This is text"

#Surnames
FATHER_SURNAME = "Perez"
MOTHER_SURNAME = "Smith"
SPANISH_CHILD_SURNAME = "Perez Smith"
FULL_NAME = "Emilio Perez"
FULL_NAME_SPANISH = "Emilio Perez Smith"
ACTUAL_NAME = "Emilio"
ACTUAL_SECOND = "Alberto"
ACTUAL_THIRD = "Camilo"

#SANDBOX Data
MAIN_SANDBOX_PROFILE = "399"
MAIN_SANDBOX_PROFILE_API = "profile-399"
MAIN_SANDBOX_WIFE = "408"
OLD_DELETED_SON = "415"
UNION_MAIN_PROFILE = "union-156"
SANDBOX_MAIN_ADDRESS = "https://sandbox.geni.com/people/Testing-Profile/1149101"
SANDBOX_MAIN_API_G = "https://sandbox.geni.com/api/profile-g1149101"
SANDBOX_MAIN_API_NOG = "https://sandbox.geni.com/api/profile-399"
MAIN_SANDBOX_PROFILE_ID = "profile-399"
FATHER_PROFILE_SANDBOX = "https://sandbox.geni.com/api/profile-g1149810"
BROTHER_PROFILE_SANDBOX = "https://sandbox.geni.com/api/profile-g1150205"
GRANDFATHER_SANDBOX = "https://sandbox.geni.com/people/GrandFather-Profile/1230605"

#Other data
GENI_INPUT_THROUGH = "https://www.geni.com/people/Leoncio-Cerro-Siguenza/6000000048574355159?through=6000000048688500197"
GENI_INPUT_THROUGH_API = "https://sandbox.geni.com/api/profile-g6000000048574355159"
GENI_WRONG_GET_METHOD =  "https://www.geni.com/api/profiles-g6000000048374355159?tokren=sfsdfsdfsdfsd"
GENI_TWO_MARRIAGES_PROFILE = "https://sandbox.geni.com/people/Tow-Marriages-Profile/1161868"
GENI_TWO_MARRIAGES_PROFILE_LINK = "https://api.sandbox.geni.com/profile-930"
#Wrong token for testing execution
WRONG_TOKEN='iSNPWCfIVKI2vH2HQLUnYppCssIMVN17kpno9ZTe'

