import openai
import torch
import db

from statistics import mean
import rmp_helpers

from config import openai_demo_key
openai.api_key = openai_demo_key

class RMPCourse:
    def __init__(self, professor, course, school='UC Irvine', summary = True):

        for row in db.get_cached():
            print(row)
            if row[1].strip().lower() == professor.split()[-1].strip().lower() and \
               row[3].strip().lower() == course.split()[-1].strip().lower():
                self.professor = row[0] + ' ' + row[1]
                self.department = row[2]
                self.course = row[3]
                self.quality = row[4]
                self.difficulty = row[5]
                self.review_summary = row[6]
                print('Fetched from database.')
                return
            
        self.school_id = rmp_helpers.get_schools_by_name(school)[0]
        self.professor = rmp_helpers.get_professors_by_school_and_name(self.school_id, professor)
        if len(self.professor) < 1: raise ValueError('No Matching Professor')
        self.professor = self.professor[0]
        self.ratings = self.professor.get_ratings()
        self.professor = self.professor.name
        self.department = ' '.join(course.split()[:-1])
        self.course = course.split()[-1]
        self.quality = self.getAverageQuality()
        self.difficulty = self.getAverageDifficulty() 
        if summary: self.review_summary = self.summarizeReviews()   

        # to_cache = (self.professor.split()[:-1], self.professor.split()[-1], self.department,
        #                  self.course, self.quality, self.difficulty, self.review_summary)

        db.insert_cached(' '.join(self.professor.split()[:-1]), self.professor.split()[-1], self.department,
                         self.course, self.quality, self.difficulty, self.review_summary)

    def formatted(self):
        return f'{self.department} {self.course} with {self.professor}'

    def getProfessorRatings(self):
        return self.ratings
    
    def _get_review_text(self):
        out = ""
        for rating in self.ratings:
            if self.course != None and str(self.course) not in rating.class_name: continue
            out += (rating.comment + '\n\n')
        return out
    
    def getAverageDifficulty(self):
        vals = []
        for rating in self.ratings:
            if self.course != None and str(self.course) not in rating.class_name: continue
            vals.append(rating.difficulty)
        return mean(vals)
        
    def getAverageQuality(self):
        vals = []
        for rating in self.ratings:
            if self.course != None and str(self.course) not in rating.class_name: continue
            vals.append(rating.rating)
        return mean(vals)

    def summarizeReviews(self):
        # LIVE: queries openai API
        messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
        message = 'Here is a list of reviews written by people, can you summarize it for me in 3 sentences?\n\n'
        messages.append({"role": "user", "content": message + self._get_review_text()})

        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", messages=messages)
        self.review_summary = chat.choices[0].message.content
        return self.review_summary
    
class Schedule:
    def __init__(self, raw_course_text):
        self.courses = []
        for raw in raw_course_text:
            course = RMPCourse(professor=raw['professor'],course=raw['course'])
            self.courses.append(course)
            
    def getCourses(self):
        return self.courses
    
    def model_prediction(self, model):
        x = torch.zeros(1,10)
        i = 0
        for course in self.courses:
            x[0:,i] = course.quality
            x[0:,5+i] = course.difficulty
        return model.predict(x).item()