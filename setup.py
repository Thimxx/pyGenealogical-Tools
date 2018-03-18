'''
Created on 10 mar. 2018

@author: Val
'''

from setuptools import setup


setup(name='pyGenealogicalTools',
      version="0.1.0",
      description="Genealogical tools",
      long_description="Some genealogical tools under development. wxpython requires manual installation",
      author='Val',
      url='https://github.com/Thimxx/pyGenealogical-Tools',
      license='GPL-3.0',
      install_requires = ['requests', 'openpyxl', 'pyexcel', 'pyexcel-xls',
                          'python-Levenshtein', 'pyexcel-xlsx', 'gedcompy'
                          ],
      )