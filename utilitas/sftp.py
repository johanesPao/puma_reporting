from paramiko import SSHClient, AutoAddPolicy, SSHException, AuthenticationException
from pathlib import Path
from utilitas.logging import log_dan_waktu
import logging

logger = logging.getLogger(__name__)


@log_dan_waktu("Transfer file ke server SFTP")
def transfer_file_sftp(
    host: str, port: str, user: str, passwd: str, sumber_file: list[str]
) -> bool:
    try:
        with SSHClient() as klien_ssh:
            klien_ssh.set_missing_host_key_policy(AutoAddPolicy())
            logger.info(f"🔗 Menghubungkan ke SFTP {host}:{port}...")

            klien_ssh.connect(
                hostname=host,
                port=port,
                username=user,
                password=passwd,
                look_for_keys=False,
                allow_agent=False,
                timeout=10,
                banner_timeout=10,
                auth_timeout=10,
            )

            logger.info("✅ Koneksi SFTP berhasil. Memulai upload...")

            with klien_ssh.open_sftp() as sftp:
                for file in sumber_file:
                    try:
                        nama_remote = Path(file).name
                        sftp.put(file, nama_remote)
                        logger.info(f"📤 Upload berhasil: {file} → {nama_remote}")
                    except Exception as e:
                        logger.error(f"⚠️ Gagal upload {file}: {e}")

        logger.info("📦 Semua file selesai diproses.")
        return True

    except AuthenticationException:
        logger.error("❌ Autentikasi SFTP gagal: Username atau password salah.")
    except SSHException as e:
        logger.error(f"❌ SSH Error: {e}")
    except EOFError:
        logger.error("❌ Koneksi SFTP ditutup oleh server (EOFError).")
    except Exception as e:
        logger.error(f"⚠️ Kesalahan tak terduga saat transfer: {e}")

    return False
