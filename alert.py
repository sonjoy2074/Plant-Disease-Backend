# from flask import Blueprint, jsonify
# from flask_mysqldb import MySQL

# # Define the alert blueprint
# alert_bp = Blueprint('alert', __name__)

# mysql = MySQL()

# @alert_bp.route('/alerts', methods=['GET'])
# def get_alerts():
#     try:
#         cursor = mysql.connection.cursor()

#         # Query to find users whose district has the same rice disease occur more than 4 times
#         query = """
#         SELECT u.id, u.name, u.email, u.district, h.prediction, COUNT(h.prediction) AS disease_count
#         FROM users u
#         JOIN history h ON u.id = h.user_id
#         GROUP BY u.district, h.prediction
#         HAVING COUNT(h.prediction) > 1
#         """
#         cursor.execute(query)
#         alerts = cursor.fetchall()

#         if not alerts:
#             return jsonify({'message': 'No alerts found'}), 200

#         # Format the alerts into a list of dictionaries
#         alert_list = []
#         for alert in alerts:
#             alert_list.append({
#                 'user_id': alert['id'],
#                 'name': alert['name'],
#                 'email': alert['email'],
#                 'district': alert['district'],
#                 'disease': alert['prediction'],
#                 'count': alert['disease_count']
#             })

#         cursor.close()

#         return jsonify({'alerts': alert_list}), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# New POST method to get alerts by district
from flask import Blueprint, jsonify, request
from flask_mysqldb import MySQL

# Define the alert blueprint
alert_bp = Blueprint('alert', __name__)

mysql = MySQL()
@alert_bp.route('/alerts/district', methods=['POST'])
def get_alerts_by_district():
    try:
        # Get the district from the request body
        data = request.json
        district = data.get('district')

        if not district:
            return jsonify({'error': 'District not provided'}), 400

        cursor = mysql.connection.cursor()

        # Query to find users in the given district whose rice disease occurred more than 3 times
        query = """
        SELECT u.id, u.name, u.email, u.district, h.prediction, COUNT(h.prediction) AS disease_count
        FROM users u
        JOIN history h ON u.id = h.user_id
        WHERE u.district = %s
        GROUP BY u.district, h.prediction
        HAVING COUNT(h.prediction) > 2
        """
        cursor.execute(query, (district,))
        alerts = cursor.fetchall()

        if not alerts:
            return jsonify({'message': f'No alerts found for district: {district}'}), 200

        # Format the alerts into a list of dictionaries
        alert_list = []
        for alert in alerts:
            alert_list.append({
                # 'user_id': alert['id'],
                # 'name': alert['name'],
                # 'email': alert['email'],
                'district': alert['district'],
                'disease': alert['prediction'],
                # 'count': alert['disease_count']
            })

        cursor.close()

        return jsonify({'alerts': alert_list}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
