DB_USER = 'root'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_DB = 'flasktest'

DEBUG = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
