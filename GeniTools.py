from pyGeni import profile
from parser_input import reader_input
from analyzefamily.ancerstors_climb import climb


data = reader_input.reader_input("INPUT")
test_profile = profile.profile(data.profile, data.genikey)



climber = climb(test_profile)
ancestors = climber.get_ancestors(4)


