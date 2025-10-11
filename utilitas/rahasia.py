import os
import logging
from dataclasses import dataclass
from infisical_sdk import InfisicalSDKClient
from utilitas.logging import log_dan_waktu

try:
    # Konstan ini hanya eksis saat proses build
    # type: ignore[import]
    from utilitas.rahasia_buildinfo import (
        ENV_HOST,
        ENV_PROJECT_ID,
        ENV_CLIENT_ID,
        ENV_CLIENT_SECRET,
    )

    ENV_MODE = None
except ImportError:
    # fallback ke lokal development
    from dotenv import load_dotenv

    load_dotenv()
    ENV_MODE = os.getenv("ENV_MODE")
    ENV_HOST = os.getenv("ENV_HOST")
    ENV_PROJECT_ID = os.getenv("ENV_PROJECT_ID")
    ENV_CLIENT_ID = os.getenv("ENV_CLIENT_ID")
    ENV_CLIENT_SECRET = os.getenv("ENV_CLIENT_SECRET")

logger = logging.getLogger(__name__)


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
    bcc: str


@log_dan_waktu("Membaca dan memuat rahasia")
class Rahasia:
    def __init__(self):
        try:
            logger.info(f"🔗 Menghubungkan ke {ENV_HOST}...")
            klien_env = InfisicalSDKClient(ENV_HOST)

            klien_env.auth.universal_auth.login(ENV_CLIENT_ID, ENV_CLIENT_SECRET)

            list_rahasia = klien_env.secrets.list_secrets(
                project_id=ENV_PROJECT_ID,
                environment_slug="dev" if ENV_MODE == "dev" else "produksi",
                secret_path="/",
                expand_secret_references=True,
            ).secrets

            logger.info("📦 Unpack rahasia ke dalam proses env...")
            if list_rahasia:
                for rahasia in list_rahasia:
                    os.environ[rahasia.secretKey] = rahasia.secretValue

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
                bcc=os.getenv("BCC_ADDRESS"),
            )
        except Exception as e:
            logger.error(f"⚠️ Gagal membaca dan memuat rahasia: {e}")
