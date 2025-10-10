from utilitas.logging import log_dan_waktu
from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass
class KredensialDatabase:
    server: str
    port: str
    database: str
    uid: str
    pwd: str


@dataclass
class KredensialSFTP:
    host: str
    port: str
    user: str
    password: str


@dataclass
class KredensialEmail:
    username: str
    password: str
    to: str
    cc: str


@log_dan_waktu("Membaca dan memuat rahasia lingkungan")
class Rahasia:
    def __init__(self):
        load_dotenv()
        self.db = KredensialDatabase(
            server=os.getenv("DB_SERVER"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_DATABASE"),
            uid=os.getenv("DB_UID"),
            pwd=os.getenv("DB_PWD"),
        )
        self.sftp = KredensialSFTP(
            host=os.getenv("SFTP_HOST"),
            port=os.getenv("SFTP_PORT"),
            user=os.getenv("SFTP_USER"),
            password=os.getenv("SFTP_PASSWORD"),
        )
        self.email = KredensialEmail(
            username=os.getenv("GMAIL_ACCOUNT"),
            password=os.getenv("GMAIL_APP_PASSWORD"),
            to=os.getenv("TO_ADDRESS"),
            cc=os.getenv("CC_ADDRESS"),
        )
