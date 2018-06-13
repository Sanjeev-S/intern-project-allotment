import unittest
from in_memory_db import InMemoryDB


class InMemoryDBTest(unittest.TestCase):

    def setUp(self):
        self.db = InMemoryDB()

    def test_get_projects(self):
        projects1 = self.db.get_projects("M1")
        projects2 = self.db.get_projects("M2")
        self.assertEqual(projects1, ["P1", "P2"])
        self.assertEqual(projects2, ["P3", "P4"])

    def test_get_students_live_null(self):
        live_map = self.db.get_students_live_for_project("P1")
        self.assertEqual(live_map["students"], [])

    def test_get_students_live_after_one_tick(self):
        self.db.force_tick()
        live_map1 = self.db.get_students_live_for_project("P1")
        live_map2 = self.db.get_students_live_for_project("P2")
        self.assertEqual(live_map1["students"], ["S1", "S2"])
        self.assertEqual(live_map2["students"], ["S4"])

    def test_get_students_live_after_two_tick(self):
        self.db.force_tick()
        self.db.force_tick()
        live_map1 = self.db.get_students_live_for_project("P1")
        live_map2 = self.db.get_students_live_for_project("P2")
        self.assertEqual(live_map1["students"], ["S1", "S2", "S3", "S4"])
        self.assertEqual(live_map2["students"], ["S1", "S2", "S3", "S4"])

    def test_select_student_after_one_tick(self):
        self.db.force_tick()
        self.db.select_student_for_project("S1", "P1")
        live_map1 = self.db.get_students_live_for_project("P1")
        live_map2 = self.db.get_students_live_for_project("P2")
        self.assertEqual(live_map1, {"fixed": True, "students": ["S1"]})
        self.assertEqual(live_map2, {"fixed": False, "students": ["S2", "S4"]})

    def test_select_two_student_after_one_tick(self):
        self.db.force_tick()
        self.db.select_student_for_project("S1", "P1")
        self.db.select_student_for_project("S2", "P2")
        live_map1 = self.db.get_students_live_for_project("P1")
        live_map2 = self.db.get_students_live_for_project("P2")
        live_map3 = self.db.get_students_live_for_project("P3")
        live_map4 = self.db.get_students_live_for_project("P4")
        self.assertEqual(live_map1, {"fixed": True, "students": ["S1"]})
        self.assertEqual(live_map2, {"fixed": True, "students": ["S2"]})
        self.assertEqual(live_map3, {"fixed": False, "students": ["S3", "S4"]})
        self.assertEqual(live_map4, {"fixed": False, "students": ["S3", "S4"]})

    def test_select_fails_for_same_after_one_try(self):
        self.db.force_tick()
        success1 = self.db.select_student_for_project("S1", "P1")
        success2 = self.db.select_student_for_project("S1", "P1")
        self.assertEqual(success1, True)
        self.assertEqual(success2, False)
