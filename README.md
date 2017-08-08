# GeniTools

![alt text](https://travis-ci.org/Thimxx/GeniTools.svg?branch=master)
![alt text](https://coveralls.io/repos/github/Thimxx/GeniTools/badge.svg?branch=master)

An interface under development for Geni based on python. 

It is mainly offering the following capabilities:

1) Access by command line to profiles and relationship information.
2) Build a tree of ancestors
3) Build a map of cousing of a given profile

# Installation instructions

Tested using python 3.6.2, happy to test other versions if needed.

In order to use the tools you will need to install the module requests: http://docs.python-requests.org/en/master/

# Usage

The file GeniTools is the one I am using as main programme. It is not yet very stable, but the libraries are getting. Just use the input file "INPUT_TEMPLATE" and select as input inside the script GeniTools.py, the input file needs to include the Geni token and the starting profile.

In order to get the token just go here: https://www.geni.com/platform/developer/api_explorer and introduce it in the input file as GENIKEY. Notice that the key gets updated almost everyday... so everytime you are using this script you will need to do it.