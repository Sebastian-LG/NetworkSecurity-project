"""
The Setup.py is an essential part of packaging
and distributing Python projects.
It is used by setuptools to define the cnfiguration
of your project such as its metadata, dependencies and more
"""
# Scan all folders and wherever there is a __init__ it will treat that as a package
# 
from setuptools import find_packages,setup
from typing import List

def get_requirements() ->List[str]:
    """
    This function will return a list of requirements
    """
    requirement_lst = []
    try:
        with open("requirements.txt",'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                #Ignore -e . and empty lines
                # -e will run the setup.py and configure the project as a package
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError as e:
        print("Requirements.txt file not found")
    
    return requirement_lst

setup(name = "NetworkSecurity",
      version = "0.0.1",
      author = "Sebastian Leon",
      author_email= "joan2613@gmail.com",
      packages=find_packages(),
      install_requires=get_requirements())
print(get_requirements())