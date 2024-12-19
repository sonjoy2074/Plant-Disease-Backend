from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from config import Config
#import logging
# Define the auth blueprint
auth_bp = Blueprint('auth', __name__)

mysql = MySQL()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'error': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']
    name = data['name']
    district = data['district']
    mobile = data['mobile']

    # Hash the password (optional, but recommended)
    # hashed_password = generate_password_hash(password)

    cursor = mysql.connection.cursor()

    # Adjust the query to insert all values: email, password, name, address, and phone
    cursor.execute(
        "INSERT INTO users (email, password, name, district, mobile) VALUES (%s, %s, %s, %s, %s)", 
        (email, password, name, district, mobile)
    )
    
    mysql.connection.commit()
    cursor.close()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'error': 'Missing email or password'}), 400

    email = data['email']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cursor.fetchone()
    cursor.close()

    # Check if user exists and passwords match (without hashing)
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['email'] = user['email']
        
        # Return user info, excluding the password
        user_info = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'district': user['district'],
            'mobile': user['mobile']
        }
        # login.logging.info(f"User logged in: {user_info}")

        return jsonify({
            'message': 'Login successful',
            'user': user_info
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return jsonify({'message': 'Logged out successfully'}), 200
