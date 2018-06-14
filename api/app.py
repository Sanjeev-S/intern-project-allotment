from flask import Flask, request, jsonify
from in_memory_db import InMemoryDB
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
db = InMemoryDB()


def handle_errors(func):
    """Decorator to handle errors"""
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except Exception as e:
            response = jsonify({"success": False, "message": str(e)})
        return response
    wrapper.func_name = func.func_name
    return wrapper


@handle_errors
@app.route('/project/<string:project_name>', methods=["POST"])
def select_student_for_project(project_name):
    if not request.json:
        raise Exception("Please provide a body with student_name")
    student_name = request.json.get('student_name')
    if not student_name:
        raise Exception("student_name missing in body")
    success = db.select_student_for_project(student_name, project_name)
    return jsonify({"success": success})


@handle_errors
@app.route('/project/<string:project_name>')
def get_live_students(project_name):
    live_map = db.get_students_live_for_project(project_name)
    return jsonify(live_map)


@handle_errors
@app.route('/manager/<string:manager_name>')
def get_projects(manager_name):
    projects = db.get_projects(manager_name)
    return jsonify(projects)

@handle_errors
@app.route('/result')
def result():
    results = db.get_results()
    return jsonify(results)

@handle_errors
@app.route('/reset')
def reset():
    global db
    db = InMemoryDB()
    return jsonify({"success": True})

@handle_errors
@app.route('/start')
def start_tick():
    success = db.start_tick()
    return jsonify({"success": success})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
