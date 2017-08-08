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