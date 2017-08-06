from pyGeni import profile
from parser_input import reader_input

data = reader_input.reader_input("INPUT")
test_profile = profile.profile(data.profile)
