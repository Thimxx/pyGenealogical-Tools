# pyGenealogical-Tools

![alt text](https://travis-ci.org/Thimxx/pyGenealogical-Tools.svg?branch=master)
![alt text](https://coveralls.io/repos/github/Thimxx/pyGenealogical-Tools/badge.svg?branch=master)
![alt text](https://api.codacy.com/project/badge/Grade/3603c4580c464d209d44401021ef8642)

Several genealogical python tools included which are under development.

It is mainly offering the following capabilities:

1) Access by command line to Geni profiles and relationship information.
2) Geni interface
* Build a tree of ancestors in Geni
* Build a map of cousins of a given profile in Geni.
* Create a child, parents or partner in geni
* Delete a profile in geni
* Get profile, relations and union data.
3) Several genealogical functions.
* Get children surname based on several naming conventions
* Get name removing surnames
* Check dates consistency in profiles
* Guess the names and surnames from a complete surname (beta)
4) A common base profile for any genealogical input
* Merging profile algorithm (basic)
5) A tool for parsing FamilySearch excel outputs of sons in a family.
* Import to Geni an excel output of children from FamilySearch records, it will merge common profiles
6) Interface with several online registers:
* Rememori: https://www.rememori.com 

Notice that this import is intended to import registers from FamilySearch, is you are interested in importing profiles from a family tree located in FamilySearch to Geni use this tool: https://github.com/jeffg2k/SmartCopy, which is a pretty nice piece of software and very helpful.

This application uses the Geni API but is not endorsed, operated, or sponsored by Geni.com.

# Installation instructions

Tested using python 3.5.3 and 3.6.2, happy to test other versions if needed. Main limitation are the testing capabilities in travis for wxpython.

In order to use the tools you will need to install the following modules:
* requests: http://docs.python-requests.org/en/master/ 
* wxpython
* metaphone: https://pypi.python.org/pypi/Metaphone/0.4 
* openpyxl
* pyexcel pyexcel-xls pyexcel-xlsx (only used for transforming xls into xlsx)
* python-Levenshtein

Concerning testing, the repository if configured to use nose, coverage, nose-htmloutput, so you will need to install in your local installation as well.

# Usage

The file GeniTools is the one I am using as main programme. It is not yet very stable, but the libraries are getting. Just use the input file "INPUT_TEMPLATE" and select as input inside the script GeniTools.py, the input file needs to include the Geni token and the starting profile.

In order to get the token just go here: https://www.geni.com/platform/developer/api_explorer and introduce it in the input file as GENIKEY. Notice that the key gets updated almost everyday... so everytime you are using this script you will need to do it.


# Interested in helping?

There are several areas where you can collaborate:

* Report any wrong behaviour as an issue
* Comment the code where it is not properly commented
* Provide naming and surname conventions for other languages
* Support on documentation development or examples
* Solve an specific issue