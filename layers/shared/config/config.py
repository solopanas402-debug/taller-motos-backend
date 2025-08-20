import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_URL = os.getenv("DB_URL")
    DB_KEY = os.getenv("DB_KEY")