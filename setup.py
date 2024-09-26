from setuptools import find_packages,setup
from typing import List

hypen_dot_e = "-e ."
def get_requirements(text_file:str)-> List[str]:
    with open(text_file, "r") as file_obj:
        requirements = file_obj.read().splitlines()

    if hypen_dot_e in requirements:
        requirements.remove(hypen_dot_e)
    return requirements


setup(
    name= "Flight Price Prediction",
    version= "0.0.1",
    description= "This is a flight price prediction app",
    long_description= "This is a user friendly flight price prediction app where user can easly predict the price of the flights and book the tickets",
    author= "Deepak Pawar",
    author_email= "deepakpw234@gmail.com",
    packages= find_packages(),
    install_req = get_requirements('requirements.txt')
)