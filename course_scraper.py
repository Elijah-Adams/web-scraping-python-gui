import requests 
from bs4 import BeautifulSoup 
from dataclasses import dataclass
import json
import re

@dataclass
class Course:
    name: str=''
    href: str=''
    text: str=''


# Making a GET request 
r = requests.get('https://omscs.gatech.edu/current-courses') 
  
# Parsing the HTML 
s = BeautifulSoup(r.content, 'html.parser') 

# Find courses
main_body = s.find('div', class_='field field--name-field-multi-body field--type-text-with-summary field--label-hidden field__item')
course_list = main_body.find('ul').find_all('li')

# Create an empty dictionary
courses = []

# Save course information
for li in course_list:
    
    # Find course information
    a = li.find('a', href=True)

    # Ignore courses without web pages
    if not a:
        continue

    # Update course information
    course_name = a.text
    course_href = a['href'][1:]

    # Making a GET request 
    url = 'https://omscs.gatech.edu/' + course_href
    r = requests.get(url) 
    
    # Parsing the HTML 
    s = BeautifulSoup(r.content, 'html.parser') 
    overview = s.find('div', class_='field field--name-field-multi-body field--type-text-with-summary field--label-hidden field__item')

    # Save web page text
    course_text = ''
    for i in overview.stripped_strings:
        course_text += ' ' + i

    # Keep alpha and numberic chars; Then remove leading, trailing, and multiple spaces
    course_text = re.sub(' +', ' ', re.sub(r'[^a-zA-Z0-9 ]+', '', course_text).lower().strip())

    # Add course
    courses.append(Course(course_name, course_href, course_text))

# Store courses in json file
listObj = []
for course in courses:
    listObj.append({
    "name": course.name,
    "href": course.href,
    "text": course.text
    })

# The json file to save the output data   
save_file = open("courses.json", "w")  
json.dump(listObj, save_file, indent = 4)  
save_file.close()  