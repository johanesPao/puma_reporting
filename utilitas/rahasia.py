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
    protocol: str
    user: str
    password: str


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
            protocol=os.getenv("SFTP_PROTOCOL"),
            user=os.getenv("SFTP_USER"),
            password=os.getenv("SFTP_PASSWORD"),
        )
