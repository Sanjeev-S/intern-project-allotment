import time
import thread

STEP = 2
SLEEP_DURATION = 30

# TODO: Does live student order matter?
# TODO: Need to make part of select student for project atomic - concurrency case
# TODO: Read this preferences and projects from a file
# TODO: After process is over(student/project list is empty maybe?), then store student-project data to file
# TODO: Admin page which can start and reset the process. Based on name of ldap user we decide if he's admin


# TODO IF TIME
# TODO: Look at session and how we can secure post calls
# TODO: Mongo DB?
class InMemoryDB:

    def __init__(self):
        self.manager_projects = {}
        self.student_preferences = {}
        self.projects = []
        self.students = []
        self.project_student_live_map = {}
        self.num_projects = 0
        self.tick = 0
        self.setup_data()

    def setup_data(self):
        self.tick = 0
        self.num_projects = 4
        self.manager_projects = {
            "M1": ["P1", "P2"],
            "M2": ["P3", "P4"]
        }
        self.projects = ["P1", "P2", "P3", "P4"]
        self.students = ["S1", "S2", "S3", "S4"]
        self.student_preferences = {
            "S1": ["P1", "P3", "P4", "P2"],
            "S2": ["P3", "P1", "P2", "P4"],
            "S3": ["P4", "P3", "P1", "P2"],
            "S4": ["P2", "P3", "P4", "P1"]
        }
        self.update_projects_map()

    def start_tick(self):
        if self.tick == 0:
            thread.start_new_thread(self.do_tick, ())
            return True
        return False

    def do_tick(self):
        for x in range(STEP, self.num_projects + 1, STEP):
            self.tick = x
            self.update_projects_map()
            time.sleep(SLEEP_DURATION)

    def force_tick(self):
        self.tick += STEP
        self.update_projects_map()

    def select_student_for_project(self, student_name, project_name):
        try:
            if student_name not in self.students or project_name not in self.projects:
                return False
            # raise key error if element not there
            del self.student_preferences[student_name]
            # raise value error if element not there
            self.students.remove(student_name)
            self.projects.remove(project_name)
            for student in self.students:
                self.student_preferences[student].remove(project_name)
            self.fix_student(student_name, project_name)
            self.update_projects_map()
            return True
        except (KeyError, ValueError):
            return False

    def get_projects(self, manager_name):
        return self.manager_projects.get(manager_name)

    def get_students_live_for_project(self, project_name):
        return self.project_student_live_map.get(project_name)

    def update_projects_map(self):
        for project in self.projects:
            live_students = [student for student in self.students
                             if project in self.student_preferences[student][:self.tick]]
            self.project_student_live_map[project] = {
                "students": live_students,
                "fixed": False
            }

    def fix_student(self, student_name, project_name):
        self.project_student_live_map[project_name] = {
            "students": [student_name],
            "fixed": True
        }






