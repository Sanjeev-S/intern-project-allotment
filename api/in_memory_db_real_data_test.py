import unittest
import in_memory_db
import os


class InMemoryDBTest(unittest.TestCase):

    def setUp(self):
        self.db = in_memory_db.InMemoryDB()

    def tearDown(self):
        results_file = in_memory_db.SAVE_FILE
        if os.path.exists(results_file):
            os.remove(results_file)

    def test_select_student(self):
        self.db.select_student_for_project("Hardik Gupta", "Building a model to forecast Calls To Unit Ratio")
        live_map1 = self.db.get_students_live_for_project("Building a model to forecast Calls To Unit Ratio")
        self.assertEqual(live_map1, {"fixed": True, "students": ["Hardik Gupta"]})