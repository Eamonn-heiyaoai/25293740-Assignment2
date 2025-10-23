from flask import Flask, jsonify, request

app = Flask(__name__)

courses = [
    {"id": 1, "code": "COMP601", "name": "Software Engineering"},
    {"id": 2, "code": "COMP604", "name": "Database Systems"}
]

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses), 200

@app.route('/courses', methods=['POST'])
def add_course():
    new_course = request.get_json()
    if not new_course.get("id") or not new_course.get("name"):
        return jsonify({"error": "Missing id or name field"}), 400
    courses.append(new_course)
    return jsonify({"message": "Course added successfully", "data": new_course}), 201

@app.route('/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    for course in courses:
        if course["id"] == course_id:
            return jsonify(course), 200
    return jsonify({"error": "Course not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
