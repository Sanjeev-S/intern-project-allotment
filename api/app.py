from flask import Flask, request, jsonify, send_from_directory, render_template
from in_memory_db import InMemoryDB
from flask_cors import CORS


app = Flask(__name__)
db = InMemoryDB()
CORS(app)


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


@app.route('/static/<string:path>')
def static_server(path):
    return send_from_directory('../static', path)


@app.route('/project/<string:project_name>', methods=["POST"])
@handle_errors
def select_student_for_project(project_name):
    if not request.json:
        raise Exception("Please provide a body with student_name")
    student_name = request.json.get('student_name')
    if not student_name:
        raise Exception("student_name missing in body")
    success = db.select_student_for_project(student_name, project_name)
    return jsonify({"success": success})


@app.route('/result')
@handle_errors
def result():
    results = db.get_results()
    columns = [
        {
            "field": "name",  # which is the field's name of data key
            "title": "Student Name",  # display as the table header's name
            "sortable": True,
        },
        {
            "field": "project",
            "title": "Project Name",
            "sortable": True,
        }
    ]
    data = []
    for project, student in results.iteritems():
        data.append({
            "name": student,
            "project": project
        })

    return render_template("table.html", data=data, columns=columns, title='Allocated Interns')


@app.route('/manager/<string:manager_name>')
@handle_errors
def get_projects_with_live_students(manager_name):
    projects = db.get_projects_with_live_students(manager_name)
    return jsonify(projects)

@app.route('/dashboard')
@handle_errors
def home():
    user = "sanjeev.s"
    return render_template("home.html", user=user)


@app.route('/reset')
@handle_errors
def reset():
    global db
    db = InMemoryDB()
    return jsonify({"success": True})


@app.route('/restart')
@handle_errors
def restart():
    global db
    db = InMemoryDB()
    success = db.start_tick()
    return jsonify({"success": success})


@app.route('/start')
@handle_errors
def start_tick():
    success = db.start_tick()
    return jsonify({"success": success})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
