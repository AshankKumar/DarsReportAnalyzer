import pdftotext
import unicodedata
import re
import subprocess

#TODO: handle cases in which the passed file is not a pdf or is not an actual dars report
# Function takes the path to a pdf and then converts it to a string
def convert_pdf_text(path):
    with open(path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    whole_report = str()

    for page in pdf:
        whole_report += page

    # If whole_report is empty then a possible case is that the dars 
    # report can't be converted and must be converted using ocrmypdf
    if not whole_report:
        subprocess.call(['bash', 'converter.sh', path])
    
    with open(path, 'rb') as f:
        pdf = pdftotext.PDF(f)

    whole_report = str()

    for page in pdf:
        whole_report += page

    return whole_report

# Function takes a dars report in string format and returns a list of unformatted strings representing that courses a student has taken or is taking
def get_courses_from_text(text):
    # Concatenates text to subbstring in text between last found occurences of 'SUMMARY OF COURSES TAKEN' and 'My Audit'
    text = text[text.rfind('SUMMARY OF COURSES TAKEN'):text.rfind('My Audit')]

    # Creats a list of all the lines in text
    lines = text.split('\n')

    # Uses regex to remove all extra spaces as well as leading spaces from a string. Example " Quick    Brown    Fox" -> "Quick Brown Fox"
    lines = [re.sub(' +', ' ', s.lstrip()) for s in lines]

    # Removes strings whose first 4 characters are not two letters followed by two digits
    # The list of courses a student has taken is in the form of [Term][Year] followed by the course and more information
    # [Term] and [Year] are represented by 2 uppercase letters and two digits respectively 
    # Therefore strings in lines that do not follow this format are not lines containing a course a student has taken and we can throw them out
    courses = [s for s in lines if re.match('[A-Z].*[A-Z][1-9][0-9]', s[0:4])]

    return courses

text = convert_pdf_text('roe3.pdf')
courses = get_courses_from_text(text)
print (courses)

 