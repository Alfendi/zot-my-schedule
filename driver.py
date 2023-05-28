import rmp_classes
import xgboost
import re
import requests
from rmp_classes import RMPCourse


def run(raw_course_input):
    print(raw_course_input)
    raw_courses = []
    for line in raw_course_input:
        s = line.replace(',', '').split()
        p = ' '.join([w.strip() for w in s[-2:]])
        c = ' '.join([w.strip() for w in s[:-2]])
        raw_courses.append({'professor': p, 'course': c})

    # Convert courses to Schedule Object
    schedule = rmp_classes.Schedule(raw_courses)

    # Get model's rating
    model = xgboost.XGBClassifier()
    model.load_model('./model.json')
    score = schedule.model_prediction(model)

    data_list = []
    for course in schedule.courses:
        head = f'{course.department} {course.course} with {course.professor}: Quality = {round(course.quality,2)}, Difficulty = {round(course.difficulty,2)}'
        body = course.review_summary
        data_list.append([head,body])

    max_diff = max(schedule.courses, key=lambda course: course.difficulty).formatted()
    low_qual = min(schedule.courses, key=lambda course: course.quality).formatted()

    return score, data_list, max_diff, low_qual


def maxDiffAlt(course_str):
    pattern = r'^([\w\s]+)\swith\s((?:\w+\s){2})'
    match = re.match(pattern, course_str)
    course = RMPCourse(course=match.group(1).strip(),professor=match.group(2).strip())

    max_diff_val = course.difficulty 
    division = 'Upper' if len(re.sub(r"\D", "", course.course)) > 2 else 'Lower'
    high_course = ''.join([char for char in str(course.course) if not char.isalpha()])
    high_course = int(high_course) - 1
    low_course = 0 if division == 'Lower' else 100
    dept = course.department.replace('&', '%26')

    url = f"https://api.peterportal.org/rest/v0/schedule/soc?term=2023%20Fall&" + \
          f"department={dept}&fullCourses=SkipFullWaitlist&courseNumber={low_course}-{high_course}&sectionType=LEC"

    response = requests.get(url).json() 

    out = None
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
                out = rmp_course
            if out == None: 
                out = rmp_course
    
    return f'Consider {out.formatted()} as an easier alternative.'

def minQualAlt(course_str):
    pattern = r'^([\w\s]+)\swith\s((?:\w+\s){2})'
    match = re.match(pattern, course_str)
    course = RMPCourse(course=match.group(1).strip(),professor=match.group(2).strip())

    min_qual_val = course.quality 
    division = 'Upper' if len(re.sub(r"\D", "", course.course)) > 2 else 'Lower'
    high_course = ''.join([char for char in str(course.course) if not char.isalpha()])
    high_course = int(high_course) - 1
    low_course = 0 if division == 'Lower' else 100
    dept = course.department.replace('&', '%26')

    url = f"https://api.peterportal.org/rest/v0/schedule/soc?term=2023%20Fall&" + \
          f"department={dept}&fullCourses=SkipFullWaitlist&courseNumber={low_course}-{high_course}&sectionType=LEC"

    response = requests.get(url).json() 

    out = None
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
                out = rmp_course
            if out == None: 
                out = rmp_course

    return f'Consider {out.formatted()} as a better alternative.'
