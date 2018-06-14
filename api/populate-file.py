import csv
import random
import json

def populateStudentPreferences(f_obj):
    projects=[]
    students = []
    managers = []
    f_obj.readline()
    for line in f_obj:
        data_list = line.split(',')


        projects.append(data_list[4][:-2])
        students.append(data_list[0])
        managers.append(data_list[3].split("@")[0])




    student_preferences={}
    for student in students:
        random_order_projects = random.sample(projects, len(projects))
        student_preferences[student] = []
        for project in random_order_projects:

            student_preferences[student].append(project)
    with open("student_preferences.txt","w") as outfile:
        json.dump(student_preferences, outfile, indent=4)

    manager_projects={}
    for manager in managers:
        manager_projects[manager] = projects[managers.index(manager)]
    with open("manager_projects.txt","w") as outfile:
        json.dump(manager_projects, outfile, indent=4)

with open("data-2.csv") as f_obj:
    populateStudentPreferences(f_obj)