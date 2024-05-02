import json
import re

# Get course.json data
f = open('courses.json')
data = json.load(f)

# Search data
while(True):

    # Get keyword input
    keyword = input("Keyword: ")
    print('--------')
    if not keyword:
        f.close()
        exit(0)

    for course in data:
        # Keep alpha and numberic chars; Then remove leading, trailing, and multiple spaces
        overview = course['text']
        if keyword in overview:
            print(course['name'])
    print()
    print()

# everything = ''
# for course in data:
#     everything += ' ' + course['text']

# everything = set(re.sub(' +', ' ', re.sub(r"[^\w\d'\s\-]+", '', everything).lower().strip()).split())

# print(everything)

# Closing file
f.close()