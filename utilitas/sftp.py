from paramiko import SSHClient, AutoAddPolicy
from pathlib import Path


def transfer_file_sftp(
    host: str, port: str, user: str, passwd: str, sumber_file: list[str]
):
    with SSHClient() as klien_ssh:
        klien_ssh.set_missing_host_key_policy(AutoAddPolicy())
        klien_ssh.connect(host, port, user, passwd, look_for_keys=False)
        with klien_ssh.open_sftp() as sftp:
            try:
                for file in sumber_file:
                    sftp.put(file, Path(file).name)
            except Exception as e:
                print(f"Terjadi kesalahan: {e}")
