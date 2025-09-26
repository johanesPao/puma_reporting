import os
from dotenv import load_dotenv

class Rahasia:
    def __init__(self):
        load_dotenv()
        self.db = {
            "server": os.getenv("DB_SERVER"),
            "port": os.getenv("DB_PORT"),
            "database": os.getenv("DB_DATABASE"),
            "uid": os.getenv("DB_UID"),
            "pwd": os.getenv("DB_PWD")
        }
        self.sftp = {
            "host": os.getenv("SFTP_HOST"),
            "port": os.getenv("SFTP_PORT"),
            "protocol": os.getenv("SFTP_PROTOCOL"),
            "user": os.getenv("SFTP_USER"),
            "pass": os.getenv("SFTP_PASS")
        }