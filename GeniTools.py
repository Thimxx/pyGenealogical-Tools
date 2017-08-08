from pyGeni import profile
from parser_input import reader_input
from analyzefamily.ancerstors_climb import climb
import requests


r = requests.get("https://www.geni.com/api/profile-g6000000000837888160?access_token=XDwK82II0kfi37VynRNWHoIVF0msvnyejNaXIbcE")
print("HOLA")
data = reader_input.reader_input("INPUT")
test_profile = profile.profile(data.profile, data.genikey)



#climber = climb(test_profile)
#ancestors = climber.get_ancestors(20)

url = test_profile.data["url"] + "/immediate-family" + "?access_token=paj8ZqEWcU8yJ3izwm0JSPFSLwADYLXMz0SfmSuI"
r = requests.get(url)


data = r.json()
     
for keydata in data["nodes"].keys():
    #is easier to go to the usions, so we filter by unions.
    if "union" in keydata:
         #Good... now we iterate per union the profiles found!
        #Now, let's create tmp variables for capturing the union information
        print(data["nodes"][keydata])