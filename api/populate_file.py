import csv
import random
import json


def populate_student_preferences(csv_file):
    csv_reader = csv.reader(csv_file)
    csv_reader.next()
    students = []
    projects = []
    manager_projects = {}
    for row in csv_reader:
        students.append(row[0])
        projects.append(row[2])
        manager_unique_name = row[1].split("@")[0]
        if not manager_projects.get(manager_unique_name):
            manager_projects[manager_unique_name] = []
        manager_projects[manager_unique_name].append(row[2])

    student_preferences = {}
    for student in students:
        student_preferences[student] = random.sample(projects, len(projects))

    with open("student_preferences.json", "w") as outfile:
        json.dump(student_preferences, outfile, indent=4)

    with open("manager_projects.json", "w") as outfile:
        json.dump(manager_projects, outfile, indent=4)


with open("data.csv") as csv_file:
    populate_student_preferences(csv_file)
