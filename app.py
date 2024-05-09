from flask import Flask, request, make_response, jsonify
import mysql.connector
from collections import OrderedDict
import bcrypt

app = Flask(__name__)

def get_db_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="proj2test",
    password="proj2password123",
    database="CourseManagement"
    )
    return mydb

def is_admin():
    user_role = request.headers.get('role')
    return user_role == 'Admin'

def is_student():
    user_role = request.headers.get('role')
    return user_role == 'Student'
 

@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

#Create Course
@app.route('/create_course', methods=['POST'])
def create_course():
    try:

        data = request.json

        course_id = data.get('courseID')
        course_name = data.get('courseName')

        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Only admins can create courses'}), 403

        db_connection = get_db_connection()
        mycursor = db_connection.cursor()
        mycursor.execute("INSERT INTO Course (courseID, courseName) VALUES (%s, %s)",
                       (course_id, course_name))
        db_connection.commit()
        mycursor.close()
        db_connection.close()

        return jsonify({'message': 'Course added successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    

#Retrieve all the courses
@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        db_connection = get_db_connection()
        mycursor = db_connection.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM Course")
        courses = mycursor.fetchall()
        return jsonify(courses)
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        mycursor.close()
        db_connection.close()

#Retrieve all the courses for a particular student
@app.route('/courses/student/<int:student_id>', methods=['GET'])
def get_courses_for_student(student_id):
    try:
        db_connection = get_db_connection()
        mycursor = db_connection.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM Enrol WHERE userID = %s", (student_id,))
        courses = mycursor.fetchall()
        if courses:
            return jsonify({'courses': courses}), 200
        else:
            return jsonify({'error': 'Courses not found for the student'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        mycursor.close()
        db_connection.close()

#Retrieve courses taught by a particular lecturer
@app.route('/courses/lecturer/<int:lecturer_id>', methods=['GET'])
def get_courses_for_lecturer(lecturer_id):
    try:
        db_connection = get_db_connection()
        mycursor = db_connection.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM Course WHERE userID = %s", (lecturer_id,))
        courses = mycursor.fetchall()
        if courses:
            return jsonify({'courses': courses}), 200
        else:
            return jsonify({'error': 'Courses not found for the lecturer'}), 404
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        mycursor.close()
        db_connection.close()

#Register for course
@app.route('/register_course', methods=['POST'])
def register_course():
    try:
        data = request.json

        course_id = data.get('courseID')
        student_id = data.get('userID')

        user_role = request.headers.get('role')

        if not is_student():
            return jsonify({'error': 'Only students can register for courses'}), 403

        db_connection = get_db_connection()
        mycursor = db_connection.cursor(dictionary=True)

        # Check if the course exists
        mycursor.execute("SELECT * FROM Course WHERE courseID = %s", (course_id,))
        course = mycursor.fetchone()
        if not course:
            return jsonify({'error': 'Course does not exist'}), 404
        mycursor.execute("INSERT INTO Enrol (userID, courseID) VALUES (%s, %s)", (student_id, course_id))
        db_connection.commit()


        mycursor.close()
        db_connection.close()

        return jsonify({'message': 'Student registered for course successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
#Retrieve members of a course
@app.route('/courses/members/<int:course_id>', methods=['GET'])
def get_course_members(course_id):
    try:
        db_connection = get_db_connection()
        mycursor = db_connection.cursor(dictionary=True)

        mycursor.execute("SELECT User.*, Enrol.courseID FROM User JOIN Enrol ON User.userID = Enrol.userID WHERE Enrol.courseID = %s", (course_id,))
        members = mycursor.fetchall()
        return jsonify(members)
    
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        mycursor.close()
        db_connection.close()


#A student/lecturer should be able to create an account.A user should be able to register with a userid and password. A user can be an admin, lecturer or student
@app.route('/register_user', methods=['POST'])
def register_user():
    conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
    cursor = conn.cursor()

    data = request.json
    userid = data.get('userID')
    fname = data.get('fname')
    lname = data.get('lname')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not userid or not password or not role:
        return jsonify({'Error': 'Please provide userid, first name, last name, email, password and role.'}), 400
    
    role = role.title()
    if role not in ['Admin', 'Lecturer', 'Student']:
        return jsonify({'Error': 'Invalid role provided. Role must be one of admin, lecturer, or student'}), 400

    cursor.execute("SELECT * FROM User WHERE userID = %s", (userid,))
    user = cursor.fetchone()

    if user:
        return jsonify({'Error': 'User already exists'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute("INSERT INTO User (userID, fname, lname, email, password, role) VALUES (%s, %s, %s, %s, %s, %s)", (userid, fname, lname, email, hashed_password, role))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'Message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login_user():
    conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
    cursor = conn.cursor()

    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'Error': 'Please provide correct email and password.'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    cursor.execute("SELECT * FROM User WHERE email = %s AND password = %s", (email,hashed_password))
    credential_exists = cursor.fetchone()

    if not credential_exists:
        return jsonify({'Error': 'Enter valid credentials'}), 400
    cursor.close()
    conn.close()
    return jsonify({'Message': 'User login successfully'}), 200

# Should be able to retrieve all calendar events for a particular course.
@app.route('/getCalendarEvents/<int:cid>',methods=['GET'])
def get_calendar_events(cid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        cs.execute(f"SELECT eventID, eventName, dueDate FROM CalendarEvent WHERE courseID={cid}")

        for eid, name, date in cs:
            cust = OrderedDict()
            cust["eventID"]= eid
            cust["eventName"]= name
            cust["dueDate"]= date
            clist.append(cust)
        cs.close()
        conn.close()
        return make_response(clist,200)
        
    except Exception as e:
        return make_response({'error':str(e)},400)

# Should be able to retrieve all calendar events for a particular date for a particular student.
@app.route('/getStudentCalendarEvents/<int:uid>/<date>',methods=['GET'])
def get_student_calendar_events(uid,date):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        cs.execute(f"SELECT cal.eventID, cal.eventName, cal.dueDate FROM CalendarEvent cal JOIN Course c ON cal.courseID=c.courseID JOIN Enrol e ON c.courseID=e.courseID WHERE e.userID={uid} AND cal.dueDate='{date}'")
        
        for eid, name, date in cs:
            cust = OrderedDict()
            cust["eventID"]= eid
            cust["eventName"]= name
            cust["dueDate"]= date
            clist.append(cust)
        cs.close()
        conn.close()
        return make_response(clist,200)
        
    except Exception as e:
        return make_response({'error':str(e)},400)

# Should be able to create calendar event for a course
@app.route('/newCalendarEvents',methods=['POST'])
def create_calendar_events():
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []

        data = request.get_json()
        cid = data.get('courseID')
        name = data.get('eventName')
        date = data.get('dueDate')

        cs.execute(f"INSERT INTO CalendarEvent (CourseID,eventName, dueDate) VALUES ('{cid}','{name}','{date}')")
        conn.commit()

        cs.close()
        conn.close()
        return make_response({"sucess":"Calendar Event added"},201)
        
    except Exception as e:
        return make_response({'error':str(e)},400)

#Should be able to retrieve all the forums for a particular course
@app.route('/forums/<int:cid>',methods=['GET'])
def get_forums(cid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []

        cs.execute(f'SELECT forumID, forumName FROM DiscussionForum WHERE courseID = {cid}')
        forums = cs.fetchall()

        if not forums:
            cs.close()
            conn.close()
            return make_response({"message":"No forums found."},201)
        else:
            for fid, name in forums:
                lst={"forumID":fid,"forumName":name}
                clist.append(lst)
        
            cs.close()
            conn.close()
            return make_response(clist,200)

    except Exception as e:
        return make_response({'error':str(e)},400)

#
@app.route('/forums/create',methods=['POST'])
def create_forum():
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()

        data = request.get_json()
        cid = data.get('courseID')
        name = data.get('forumName')

        cs.execute(f"INSERT INTO DiscussionForum (CourseID, forumName) VALUES ('{cid}','{name}')")
        conn.commit()
        cs.close()
        conn.close()
        return make_response({"sucess":"Forum Created"},201)

    except Exception as e:
        return make_response({'error':str(e)},400)

#Should be able to retrieve all the discussion threads for a particular forum.
@app.route('/forums/<int:fid>/threads',methods=['GET'])
def get_threads(fid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        cs.execute("SELECT threadID, title, content FROM DiscussionThread WHERE forumID={fid}")
        threads = cs.fetchall()

        if not threads:
            cs.close()
            conn.close()
            return make_response({"message":"No threads found."},201)
        else:
            for tid, title, content in threads:
                lst={"threadID":tid,"title":title,"content":content}
                clist.append(lst)
        
            cs.close()
            conn.close()
            return make_response(clist,200)

        
    except Exception as e:
        return make_response({'error':str(e)},400)

#Should be able to add a new discussion thread to a forum. Each discussion thread should have a title and the post that started the thread.
@app.route('/forums/<int:fid>/threads/create',methods=['POST'])
def create_thread(fid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        cs.execute(f"INSERT INTO DiscussionThread (forumID, parentThreadID, title, content) VALUES ('{fid}',1,'{title}','{content}')")
        conn.commit()
        cs.close()
        conn.close()

        return make_response({"sucess":"Thread Created"},201)

    except Exception as e:
        return make_response({'error':str(e)},400)

# Users should be able to reply to a thread and replies can have replies.
@app.route('/threads/<int:tid>/reply',methods=['POST'])
def reply_thread(tid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        
        data = request.get_json()
        content = data.get('content')

        cs.execute(f"INSERT INTO DiscussionThread (forumID, parentThreadID, title, content) VALUES ((SELECT forumID FROM DiscussionThread where threadID={tid}),'{tid}','','{content}')")

        conn.commit()
        cs.close()
        conn.close()
        return make_response({"sucess":"Reply added successfully"},201)

    except Exception as e:
        return make_response({'error':str(e)},400)

#A lecturer should have the ability to add course content. Course content can includes links, files, slides. Course content is separated by sections.
@app.route('/course/<int:cid>/section/<int:sid>/add',methods=['POST'])
def add_content(cid,sid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        
        data = request.get_json()
        itype = data.get('itemType')
        content = data.get('content')

        cs.execute(f"INSERT INTO SectionItem (sectionID, itemType, content) VALUES ('{sid}','{itype}','{content}')")
        conn.commit()

        cs.close()
        conn.close()

        return make_response({"sucess":"Content Added"},201)

    except Exception as e:
        return make_response({'error':str(e)},400)

# Should be able to retrieve all the course content for a particular course.
@app.route('/course/<int:cid>/section',methods=['GET'])
def get_content(cid,sid):
    try:
        conn = mysql.connector.connect(host = 'localhost',user = 'proj2test',password = 'proj2password123',database = 'CourseManagement')
        cs = conn.cursor()
        clist = []
        
        cs.execute(f"SELECT sid.itemID, sid.itemType, sid.content FROM SectionItem sid JOIN Section s ON sid.sectionID = s.sectionID WHERE s.courseID = {cid} ")
        content = cs.fetchall()

        if not content:
            cs.close()
            conn.close()
            return make_response({"message":"No content found."},201)
        else:
            for sid, itype, content in threads:
                lst={"contentID":sid,"itemType":title,"content":content}
                clist.append(lst)
        
            cs.close()
            conn.close()
            return make_response(clist,200)

    except Exception as e:
        return make_response({'error':str(e)},400)

if __name__ == '__main__':
    app.run(debug=True)
