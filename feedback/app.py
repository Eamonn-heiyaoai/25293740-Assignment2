from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

STUDENT_SERVICE = os.getenv("STUDENT_SERVICE", "http://student-profile:5000")
COURSE_SERVICE = os.getenv("COURSE_SERVICE", "http://course-catalogue:5000")

feedback_list = []

@app.route('/feedback', methods=['POST'])
def submit_feedback():

    data = request.get_json()

    if not data or not data.get("student_id") or not data.get("course_id") or not data.get("comment"):
        return jsonify({"error": "Missing student_id, course_id or comment"}), 400

    feedback_list.append(data)

    try:
        student_response = requests.get(f"{STUDENT_SERVICE}/students").json()
        course_response = requests.get(f"{COURSE_SERVICE}/courses").json()
    except Exception as e:
        return jsonify({"message": "Feedback stored but failed to fetch other data", "error": str(e)}), 500

    return jsonify({
        "message": "Feedback received!",
        "feedback": data,
        "student_count": len(student_response),
        "course_count": len(course_response)
    }), 201

@app.route('/feedback', methods=['GET'])
def get_all_feedback():
    return jsonify(feedback_list), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
