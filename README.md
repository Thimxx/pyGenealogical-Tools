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
* Extract the tree of descendants of a profile in gedcom
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
* Obituary from this newspaper: http://esquelas.elnortedecastilla.es/
7) Transformation to GEDCOM profile
* Transforms profile into elements of GEDCOM, allows to create a GEDCOM
8) Automatic investigation
* For those interfaces avaialble, it can found potential matches in a GEDCOM.

Notice that this import is intended to import registers from FamilySearch, is you are interested in importing profiles from a family tree located in FamilySearch to Geni use this tool: https://github.com/jeffg2k/SmartCopy, which is a pretty nice piece of software and very helpful.

This application uses the Geni API but is not endorsed, operated, or sponsored by Geni.com.

# Installation instructions

You can install it using pip

    pip install pyGenealogicalTools

Tested using python 3.5.3 and 3.6.2, happy to test other versions if needed. Main limitation are the testing capabilities in travis for wxpython.

In order to use the tools you will need to install the following modules:
* requests: http://docs.python-requests.org/en/master/ 
* wxpython
* metaphone: https://pypi.python.org/pypi/Metaphone/0.4 
* openpyxl
* pyexcel pyexcel-xls pyexcel-xlsx (only used for transforming xls into xlsx)
* python-Levenshtein
* gedcompy https://pypi.python.org/pypi/gedcompy | https://github.com/rory/gedcompy/
* googlemaps

All the previous modules are available in the requirements.txt file, but wxpython needs to be manually installed, visit wxpython page for further info.

Concerning testing, the repository if configured to use nose, coverage, nose-htmloutput, so you will need to install in your local installation as well.

### Geni KEY

In order to use the interface, you will need to generate an application card inside Geni and obtain a key. You can create the application card in this: location https://www.geni.com/platform/developer/api_explorer, the key will be only valid for 24h, so you will need to register again the key regularly.

For each execution of the Geni API contained in this software, you will later need to introduce the key. Do not make the key public. In the examples area you have a description of how to obtain the key in execute the complete module, in a nutshell this is the way to set the Geni Key:


    from pyGeni import set_token
    GENI_KEY = "IntroduceHereYourGeniKey"
    set_token(GENI_KEY)

### Google Key API

One of the packages used is googlemaps, which wraps the Google Maps API. However this library requires the use of a google maps API to work.

It has been found that not having a google API KEY creates random crashes and wrong values, so it is strongly recommended to use the KEY. To get the key just follow these intructions (same instructions for googlemaps api https://github.com/googlemaps/google-maps-services-python/blob/master/README.md):

 1. Visit https://developers.google.com/console and log in with
    a Google Account.
 1. Select one of your existing projects, or create a new project.
 1. Enable the API(s) you want to use. The Python Client for Google Maps Services
    accesses the following APIs:
    * Directions API
    * Distance Matrix API
    * Elevation API
    * Geocoding API
    * Geolocation API
    * Places API
    * Roads API
    * Time Zone API
 1. Create a new **Server key**.
 1. If you'd like to restrict requests to a specific IP address, do so now.
 
 Finally you need to transfer to pyGenealogyTools the variable value. There are 2 ways:
 
 1. Introduce an environmental variable called GOOGLE_API with the value
 1. Use the functions pyGenealogy.set_google_key() to set up the value of the API KEY.

Without the key, pyGenealogyTools will work, but it is prone to errors due to lack of a key, so be aware in case you are using it extensively. Better description of the issue can be found here: https://stackoverflow.com/questions/48488693/unstable-behaviour-of-google-maps-api

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