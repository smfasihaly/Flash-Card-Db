import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASEDIR = basedir
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    EXCEL_FILE_PATH = os.path.join(basedir, 'data', 'words.xlsx')
