from flask import Flask, jsonify, request, make_response #
import mysql.connector 

app = Flask(__name__)

# Connect to the database
conn = mysql.connector.connect(host='localhost',user='proj2test',password='proj2password123',database='CourseManagement')
cursor = conn.cursor()

# Endpoint for a student to submit an assignment for a course
@app.route('/assignments/submit', methods=['POST'])
def submit_assignment():
    try:
        data = request.json
        cID = data.get('courseID')
        sID = data.get('studentID')
        submission = data.get('submission')

        if not all([cID, sID, submission]):
            return jsonify({'error': 'Missing required fields'}), 400

        cursor.execute('''
            INSERT INTO Assignment (courseID, studentID, submission)
            VALUES (%s, %s, %s)
        ''', (cID, sID, submission))
        conn.commit()
        return jsonify({'message': 'Assignment submitted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint for a lecturer to submit a grade for a student's assignment
@app.route('/assignments/grade', methods=['POST'])
def submit_grade():
    try:
        data = request.json
        aID = data.get('assignmentID')
        grade = data.get('grade')

        if not all([aID, grade]):
            return jsonify({'error': 'Missing required fields'}), 400

        cursor.execute('''
            UPDATE Assignment
            SET grade = %s
            WHERE assignmentID = %s
        ''', (grade, aID))
        conn.commit()
        return jsonify({'message': ' submission successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve all courses with 50 or more students
@app.route('/reports/courses/50students', methods=['GET'])
def course_50_students():
    try:
        cursor.execute('''
            SELECT c.courseID, c.courseName, COUNT(e.userID) AS num_students
            FROM Course c
            JOIN Enrol e ON c.courseID = e.courseID
            GROUP BY c.courseID
            HAVING num_students >= 50
        ''')
        courses = cursor.fetchall()
        return jsonify({'courses': courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve all students with 5 or more courses
@app.route('/reports/students/5courses', methods=['GET'])
def students_5_courses():
    try:
        cursor.execute('''
            SELECT e.userID, COUNT(e.courseID) AS num_courses FROM Enrol e GROUP BY e.userID HAVING num_courses >= 5
        ''')
        stdts = cursor.fetchall()
        return jsonify({'students': stdts}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve all lecturers with 3 or more courses
@app.route('/reports/lecturers/3courses', methods=['GET'])
def get_lecturers_3_courses():
    try:
        cursor.execute('''
            SELECT e.userID, COUNT(e.courseID) AS num_courses
            FROM Enrol e
            JOIN User u ON e.userID = u.userID
            WHERE u.role = 'lecturer'
            GROUP BY e.userID
            HAVING num_courses >= 3
        ''')
        lecturers = cursor.fetchall()
        return jsonify({'lecturers': lecturers}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve the 10 most enrolled courses
@app.route('/reports/courses/top10enrolled', methods=['GET'])
def get_top_10_enrolled_courses():
    try:
        cursor.execute('''
            SELECT c.courseID, c.courseName, COUNT(e.userID) AS num_students
            FROM Course c
            JOIN Enrol e ON c.courseID = e.courseID
            GROUP BY c.courseID
            ORDER BY num_students DESC
            LIMIT 10
        ''')
        top_courses = cursor.fetchall()
        return jsonify({'courses': top_courses}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to retrieve the top 10 students with the highest overall averages
@app.route('/reports/students/top10averages', methods=['GET'])
def get_top_10_students_averages():
    try:
        cursor.execute('''
            SELECT e.userID, AVG(a.grade) AS average_grade
            FROM Enrol e
            JOIN Assignment a ON e.userID = a.studentID
            GROUP BY e.userID
            ORDER BY average_grade DESC
            LIMIT 10
        ''')
        top_students = cursor.fetchall()
        return jsonify({'students': top_students}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
