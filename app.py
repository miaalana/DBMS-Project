from flask import Flask, request, jsonify
import mysql.connector
import bcrypt


app = Flask(__name__)


connection = mysql.connector.connect(
    host="localhost",
    user="comp3161",
    password="password",
    database="CourseManagement"
)

cursor = connection.cursor()


@app.route('/register_user', methods=['POST'])
def register_user():
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
    connection.commit()
    cursor.close()
    connection.close() 
    
    return jsonify({'Message': 'User registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)