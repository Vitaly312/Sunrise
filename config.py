import os
from dotenv import load_dotenv


load_dotenv()
load_dotenv('.env.example')

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_PROD")