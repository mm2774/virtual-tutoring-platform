import json

import requests

SEMESTER = "FA20"

def get_subjects():
    url = 'https://classes.cornell.edu/api/2.0/config/subjects.json'
    params = {'roster': SEMESTER}
    r = requests.get(url, params=params)
    resp = r.json()

    sub_list = []
    for subject in resp['data']['subjects']:
        sub_list.append(subject['value'])
    return sub_list 

def get_subject_courses(subject, courses_list):
    url = 'https://classes.cornell.edu/api/2.0/search/classes.json'
    params = {'roster': SEMESTER, 'subject': subject}
    r = requests.get(url, params=params)
    resp = r.json()

    for course in resp['data']['classes']:
        course_data = dict() 
        course_data['subject'] = course['subject']
        course_data['number'] = course['catalogNbr']
        course_data['name'] = course['titleShort']
        courses_list.append(course_data)

def create_json():
    subject_list = get_subjects() 
    print("Number of subjects: ", len(subject_list))

    with open('subjects.json', 'w') as f:
        json.dump(subject_list, f)
    
    courses_data = []
    for subject in subject_list:
        get_subject_courses(subject, courses_data)

    filter_list = []
    for course in courses_data:
        num = int(course['number'])
        if num < 5000:
            name = course['name']
            if "Internship" not in name:
                if "Independent Study" not in name:
                    if "Undergrad Teaching Assistant" not in name:
                        if "Undergraduate Research" not in name:
                            if "Ind Study" not in name:
                                if "Senior Essay" not in name:
                                    if "Senior Capstone" not in name:
                                        if "Independent Research" not in name:
                                            if "Indep Study" not in name:
                                                if "Individual Study" not in name:
                                                    if "Teaching Experience" not in name:
                                                        if "Independent Undergraduate" not in name:
                                                            if "Ind. Undergrad." not in name:
                                                                if "Individual Study" not in name:
                                                                    if "Independent Reading & Research" not in name:
                                                                        if "Independent Project" not in name:
                                                                            if "Indvdl Study" not in name:
                                                                                if "Individu Study" not in name:
                                                                                    if "Indiv Study" not in name:
                                                                                        if "Undergraduate Teaching" not in name:
                                                                                            filter_list.append(course)

    format_list = []
    for i in range(len(filter_list)):
        cdata = dict() 
        cdata['model'] = "meetings.course"
        # slug = "{}{}".format(filter_list[i]['subject'], filter_list[i]['number'])
        # cdata['pk'] = slug
        cdata['pk'] = i + 1 
        cdata['fields'] = filter_list[i]
        desc = "{}{} {} {} {}".format(filter_list[i]['subject'], filter_list[i]['number'], filter_list[i]['subject'], filter_list[i]['number'], filter_list[i]['name'])
        cdata['fields']['description'] = desc
        format_list.append(cdata)
    
    print("Number of courses: ", len(format_list))
    with open('courses.json', 'w') as cf:
        json.dump(format_list, cf, indent=2)
    
    print('done')

create_json() 
