# history.py
from flask import Blueprint, request, jsonify
from flask_mysqldb import MySQL

# Define the history blueprint
history_bp = Blueprint('history', __name__)

mysql = MySQL()

@history_bp.route('/history', methods=['POST'])
def get_history():
    data = request.json
    if not data or 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400

    user_id = data['user_id']

    cursor = mysql.connection.cursor()
    
    # Query to fetch history for the given user_id
    cursor.execute("SELECT * FROM history WHERE user_id = %s", (user_id,))
    history_records = cursor.fetchall()
    cursor.close()

    if not history_records:
        return jsonify({'message': 'No history found for this user.'}), 404

    # Format the response data
    # history_list = []
    # for record in history_records:
    #     history_list.append({
    #         'user_id': record[1],  # Assuming user_id is the first column
    #         'prediction': record[2],  # Assuming prediction is the second column
    #         'image': record[3],  # Assuming image is the third column
    #         'timestamp': record[4]  # Assuming timestamp is the fourth column
    #     })

    return jsonify({'history': history_records}), 200
