import rmp_classes
import xgboost
import re
import requests
from rmp_classes import Schedule, RMPCourse

def run(raw_course_input = None):
    # Get courses from frontend
    # Format: list of dicts:  [ {'professor':prof1, 'course':course1},
    #                           {'professor':prof2, 'course':course2} ]
    raw_courses = [{'professor': 'Michael Shindler', 'course': 'COMPSCI 161'},
                   {'professor': 'Charless Fowlkes', 'course': 'COMPSCI 116'},
                   {'professor': 'Jennifer Wong-Ma', 'course': 'I&C SCI 51'}]

    # Convert courses to Schedule Object
    schedule = rmp_classes.Schedule(raw_courses)

    # Get model's rating 
    model = xgboost.XGBClassifier()
    model.load_model('/home/alfendi/PycharmProjects/zotmyschedule/rmp/model.json')
    score = schedule.model_prediction(model)
    
    # Output individual ratings, joint rating, alternatives, rmp summary
    print('Overall Score:' + str(score))
    for course in schedule.courses:
        print(f'{course.department} {course.course} with {course.professor}: Q={course.quality}, D={course.difficulty}')
        print('Summary:\n', course.review_summary, '\n')


def maxDiffAlt(course = None):
    max_diff_val = course.difficulty 
    division = 'Upper' if len(re.sub(r"\D", "", course.course)) > 2 else 'Lower'
    high_course = ''.join([char for char in str(course.course) if not char.isalpha()])
    high_course = int(high_course) - 1
    low_course = 0 if division == 'Lower' else 100
    dept = course.department.replace('&', '%26')

    url = f"https://api.peterportal.org/rest/v0/schedule/soc?term=2023%20Fall&" + \
          f"department={dept}&fullCourses=SkipFullWaitlist&courseNumber={low_course}-{high_course}&sectionType=LEC"

    response = requests.get(url).json() 

    default = None
    for possible_course in reversed(response['schools'][0]['departments'][0]['courses']):
        num = possible_course['courseNumber']
        for sec in possible_course['sections']:
            prof = sec['instructors'][0]
            prof = prof.replace(".", "")
            try: 
                rmp_course = RMPCourse(prof, num, summary = False)
            except ValueError as e:
                print(e)
            print(rmp_course.difficulty)
            if rmp_course.difficulty < max_diff_val:
                return f'Replacment: {course.department} {num} with {rmp_course.professor}'
            if default == None: 
                default = f'Replacment: {course.department} {num} with {rmp_course.professor}'
    return default

def minQualAlt(course = None):
    min_qual_val = course.quality 
    division = 'Upper' if len(re.sub(r"\D", "", course.course)) > 2 else 'Lower'
    high_course = ''.join([char for char in str(course.course) if not char.isalpha()])
    high_course = int(high_course) - 1
    low_course = 0 if division == 'Lower' else 100
    dept = course.department.replace('&', '%26')

    url = f"https://api.peterportal.org/rest/v0/schedule/soc?term=2023%20Fall&" + \
          f"department={dept}&fullCourses=SkipFullWaitlist&courseNumber={low_course}-{high_course}&sectionType=LEC"

    response = requests.get(url).json() 

    default = None
    for possible_course in reversed(response['schools'][0]['departments'][0]['courses']):
        num = possible_course['courseNumber']
        for sec in possible_course['sections']:
            prof = sec['instructors'][0]
            prof = prof.replace(".", "")
            try: 
                rmp_course = RMPCourse(prof, num, summary = False)
            except ValueError as e:
                print(e)
            print(rmp_course.quality)
            if rmp_course.quality > min_qual_val:
                return f'Replacment: {course.department} {num} with {rmp_course.professor}'
            if default == None: 
                default = f'Replacment: {course.department} {num} with {rmp_course.professor}'
    return default 


def alternatives(schedule = None):
    max_diff = max(schedule.courses, key = lambda course : course.difficulty)
    low_qual = min(schedule.courses, key = lambda course : course.quality)

    diff_alt = maxDiffAlt(max_diff)
    qual_alt = minQualAlt(low_qual)

    return f'{max_diff.formatted()} is your hardest course. Consider {diff_alt.formatted()} as an easier alternative.\n' + \
           f'{low_qual.formatted()} has your lowest quality professor. Consider {qual_alt.formatted()} as an better alternative.\n'



run()