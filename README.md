# GeniTools
An interface for working using python with Geni.

# Installation instructions

Tested using python 3.6.2. You need to have installed the module requests: http://docs.python-requests.org/en/master/

Each user should have its one Geni token, use the following interface to get your token: https://www.geni.com/platform/developer/api_explorer

For implementing the Geni Token, you should go to folder geni_reader and copy the file "geni_seetings_template" as "geni_settings" and replace the value of variable TOKEN

# Usage

For the moment only reading a Geni profile is available. Juse use the input file "INPUT_TEMPLATE" and select as input on the script GeniTools.py

You shall also get your local token for executing Geni, you get the token as a temporary value, so you will need to introduce it almost everyday, just get the value here: https://www.geni.com/platform/developer/api_explorer and introduce it in the input file as GENIKEY
