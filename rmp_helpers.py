# Slightly modified version of some functions 
# from the ratemyprofessor library. 
# Reflects updated url scheme for the website.

import re
import requests
import base64
from ratemyprofessor.school import School
from ratemyprofessor.professor import Professor

def get_schools_by_name(school_name: str):
    """
    Gets a list of Schools with the specified name.

    This only returns up to 20 schools, so make sure that the name is specific.
    For instance, searching "University" will return more than 20 schools, but only the first 20 will be returned.

    :param school_name: The school's name.
    :return: List of schools that match the school name. If no schools are found, this will return an empty list.
    """
    school_name.replace(' ', '+')
    url = "https://www.ratemyprofessors.com/search/schools?q=%s" % school_name
    page = requests.get(url)
    data = re.findall(r'"legacyId":(\d+)', page.text)
    school_list = []

    for school_data in data:
        try:
            school_list.append(School(int(school_data)))
        except ValueError:
            pass
    
    return school_list

def get_professors_by_school_and_name(college: School, professor_name: str):
    """
    Gets a list of professors with the specified School and professor name.

    This only returns up to 20 professors, so make sure that the name is specific.
    For instance, searching "Smith" with a school might return more than 20 professors,
    but only the first 20 will be returned.

    :param college: The professor's school.
    :param professor_name: The professor's name.
    :return: List of professors that match the school and name. If no professors are found,
             this will return an empty list.
    """
    # professor_name.replace(' ', '+')
    url = "https://www.ratemyprofessors.com" \
          "/search/teachers?q=%s&sid=%s" % (professor_name, base64.b64encode(("School-%s" % college.id)
                                                                                 .encode('ascii')).decode('ascii'))
    page = requests.get(url)
    data = re.findall(r'"legacyId":(\d+)', page.text)
    professor_list = []

    for professor_data in data:
        try:
            professor_list.append(Professor(int(professor_data)))
        except ValueError:
            pass

    return professor_list