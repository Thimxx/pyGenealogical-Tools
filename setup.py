'''
Created on 10 mar. 2018

@author: Val
'''

import setuptools

long_description=""
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='pyGenealogicalTools',
      version="0.2.0",
      description="Genealogical tools",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Val',
      packages=setuptools.find_packages(),
      url='https://github.com/Thimxx/pyGenealogical-Tools',
      license='GPL-3.0',
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",],
      install_requires = ['requests', 'openpyxl', 'pyexcel', 'pyexcel-xls',
                          'python-Levenshtein', 'pyexcel-xlsx', 'metaphone'
                          ],
      )