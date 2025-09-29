from mssql_python import Connection, connect
from pandas import DataFrame


def buka_koneksi(
    server: str, port: str, database: str, uid: str, pwd: str
) -> Connection:
    string_koneksi = (
        f"SERVER={server},{port};DATABASE={database};UID={uid};PWD={pwd};Encrypt=no"
    )
    print(string_koneksi)
    return connect(string_koneksi)


def eksekusi_kueri(koneksi: Connection, query: str) -> DataFrame:
    kursor = koneksi.cursor()
    kursor.execute(query)
    hasil = kursor.fetchall()
    kolom = [kol[0] for kol in kursor.description]
    return DataFrame(hasil, columns=kolom)


def tutup_koneksi(koneksi: Connection) -> None:
    koneksi.close()
