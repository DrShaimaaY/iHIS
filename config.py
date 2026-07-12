import os

class Config:
    # Secret Key for the site.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ihis-secret-key-2024'
    
    # DataBase
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ihis.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False