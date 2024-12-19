# config.py
class Config:
    SECRET_KEY = 'your_secret_key'  # Change this to a strong secret key
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'rice_disease_db'
    MYSQL_CURSORCLASS = 'DictCursor'
    UPLOAD_FOLDER = 'uploads'
