from mssql_python import Connection, connect
from pandas import DataFrame

def buka_koneksi(
    server: str,
    port: str,
    database: str,
    uid: str,
    pwd: str
) -> Connection:
    string_koneksi = (
        f"SERVER={server},{port};"
        f"DATABASE={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        f"Encrypt=no"
    )
    print(string_koneksi)
    return connect(string_koneksi)

def eksekusi_query(
    koneksi: Connection,
    query: str
) -> DataFrame:
    kursor = koneksi.cursor()
    kursor.execute(query)
    hasil = kursor.fetchall()
    kolom = [kol[0] for kol in kursor.description]
    return DataFrame(hasil, columns=kolom)

def tutup_koneksi(
    koneksi: Connection
) -> None:
    koneksi.close()
