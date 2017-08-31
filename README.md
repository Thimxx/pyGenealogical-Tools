# GeniTools

![alt text](https://travis-ci.org/Thimxx/GeniTools.svg?branch=master)
![alt text](https://coveralls.io/repos/github/Thimxx/GeniTools/badge.svg?branch=master)
![alt text](https://api.codacy.com/project/badge/Grade/3603c4580c464d209d44401021ef8642)

Several genealogical python tools included which are under development.

It is mainly offering the following capabilities:

1) Access by command line to Geni profiles and relationship information.
2) Geni interface
    2.1) Build a tree of ancestors in Geni
    2.2) Build a map of cousins of a given profile in Geni.
    2.3) Create a child in geni
    2.4) Delete a profile in geni
3) Several genealogical functions.
    3.1) Get children surname based on several naming conventions
    3.2) Get name removing surnames
    3.3) Check dates consistency in profiles
4) A common base profile for any genealogical input
5) A tool for parsing FamilySearch excel outputs of sons in a family.

This application uses the Geni API but is not endorsed, operated, or sponsored by Geni.com.

# Installation instructions

Tested using python 3.5.3 and 3.6.2, happy to test other versions if needed. Main limitation are the testing capabilities in travis for wxpython.

In order to use the tools you will need to install the module requests: http://docs.python-requests.org/en/master/

Concerning testing, the repository if configured to use nose, coverage, nose-htmloutput, so you will need to install in your local installation as well.

# Usage

The file GeniTools is the one I am using as main programme. It is not yet very stable, but the libraries are getting. Just use the input file "INPUT_TEMPLATE" and select as input inside the script GeniTools.py, the input file needs to include the Geni token and the starting profile.

In order to get the token just go here: https://www.geni.com/platform/developer/api_explorer and introduce it in the input file as GENIKEY. Notice that the key gets updated almost everyday... so everytime you are using this script you will need to do it.