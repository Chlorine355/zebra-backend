import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
YANDEX_GEOCODER_KEY = os.getenv('YANDEX_GEOCODER_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
MAX_DAILY_REPORTS = 5
PAGE_SIZE = 20

SMTP_FROM = os.getenv('SMTP_FROM')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
BASE_URL = os.getenv('BASE_URL')