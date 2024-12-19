from flask import Flask
from auth import auth_bp
from predict import predict_bp
from config import Config
from flask_mysqldb import MySQL
from history import history_bp
from alert import alert_bp
app = Flask(__name__)
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(predict_bp)
app.register_blueprint(history_bp)
app.register_blueprint(alert_bp)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
