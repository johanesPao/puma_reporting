from sqlalchemy import Connection, create_engine
import urllib
from pandas import DataFrame, read_sql


def buka_koneksi(
    server: str, port: str, database: str, uid: str, pwd: str
) -> Connection:
    string_koneksi = urllib.parse.quote_plus(
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server},{port};"
        f"Database={database};"
        f"UID={uid};"
        f"PWD={pwd};"
        f"Encrypt=no;"
        f"TrustServerCertificate=yes;"
    )

    return create_engine(f"mssql+pyodbc:///?odbc_connect={string_koneksi}").connect()


def eksekusi_kueri(koneksi: Connection, query: str) -> DataFrame:
    return read_sql(query, koneksi)


def tutup_koneksi(koneksi: Connection) -> None:
    koneksi.close()
