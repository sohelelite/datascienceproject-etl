'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str] :
    '''
    Function will return list of requirement
    '''
    requirement_lst : List[str] = []

    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print(f"requirements.txt file not found")

    return requirement_lst

setup(
    name= "DataScienceProject ETL",
    version= "0.0.0.1",
    author= "Sohel Shaikh",
    author_email= "sohel.shaikh.s@gmail.com",
    packages= find_packages(),
    install_requires = get_requirements()
)
        