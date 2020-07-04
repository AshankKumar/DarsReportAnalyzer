import parser
from course import course
from collections import OrderedDict
import sys

def filter_classes(classes : list):
    # filter out classes with course numbers such as 1--
    classes = filter(lambda x: '--' not in x[1], classes)
    classes = list(classes)

    # filter out duplicates courses
    classes = list(OrderedDict.fromkeys(classes))
    return classes

def put_into_courses(courses : list):
    list_of_courses = []
    for tup in courses:
        list_of_courses.append(course(tup[0], int(tup[1]), int(float(tup[2]))))
    return list_of_courses

try:
    f = open(sys.argv[len(sys.argv) - 1])
except FileNotFoundError:
    print("Give a valid path!")
finally:
    f.close()

text = parser.convert_pdf_text(sys.argv[len(sys.argv) - 1])
courses = parser.get_courses_from_text(text)
courses_num_grade_hours = parser.get_courses_num_grade_and_hours(courses)

# filter result before returning it
courses = filter_classes(courses_num_grade_hours)
courses = put_into_courses(courses)

print(*courses, sep = '\n')