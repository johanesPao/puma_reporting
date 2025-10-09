import shutil
from pathlib import Path
from datetime import datetime, timedelta
from mssql_python import Connection
import pandas as pd
from utilitas.logging import log_dan_waktu
from utilitas.eval_argumen import ModeScript
from utilitas.rahasia import KredensialDatabase
from dateutil.parser import parse
from koneksi.mssql import buka_koneksi, eksekusi_kueri
from kueri.mssql import get_kueri_sales, get_kueri_inventori

FOLDER_DASAR_OUTPUT = Path("output")
HARI_RETENSI = 28


def setup_folder_output() -> Path:
    # Pastikan FOLDER_DASAR_OUTPUT ada
    FOLDER_DASAR_OUTPUT.mkdir(exist_ok=True)

    # Buat folder dengan tanggal hari ini
    tanggal_hari_ini = datetime.today().strftime("%Y_%m_%d")
    folder_output = FOLDER_DASAR_OUTPUT / tanggal_hari_ini
    folder_output.mkdir(exist_ok=True)

    # Bersihkan folder lama yang lebih tua dari HARI_RETENSI
    tanggal_batas = datetime.today() - timedelta(days=HARI_RETENSI)
    for folder in FOLDER_DASAR_OUTPUT.glob("*"):
        try:
            tanggal_folder = datetime.strptime(folder.name, "%Y_%m_%d")
            if tanggal_folder < tanggal_batas:
                shutil.rmtree(folder)
                print(f"🗑️ Menghapus folder lama: {folder.name}")
        except ValueError:
            # Lewati folder yang tidak sesuai format tanggal
            continue

    return folder_output


def simpan_csv(data, nama_file: str, folder_output: Path) -> Path:
    path_file = folder_output / nama_file
    data.to_csv(path_file, index=False, encoding="utf-8-sig")
    return path_file


def get_data(koneksi: Connection, tipe_laporan: str, tanggal: str) -> pd.DataFrame:
    match tipe_laporan:
        case "sales":
            return eksekusi_kueri(koneksi, get_kueri_sales(tanggal))
        case "inventory":
            return eksekusi_kueri(koneksi, get_kueri_inventori(tanggal))


def generate(mode: ModeScript, db: KredensialDatabase) -> list[Path]:
    folder_output = setup_folder_output()
    csv_terbentuk: list[Path] = []

    for tipe in mode.tipe_laporan:
        df_satufile = pd.DataFrame()

        for tanggal in mode.tanggal:
            nama_proses = f"Menarik data {tipe} untuk tanggal {tanggal}"

            @log_dan_waktu(nama_proses)
            def proses_tanggal() -> None:
                with buka_koneksi(
                    db.server, db.port, db.database, db.uid, db.pwd
                ) as koneksi:
                    data = get_data(koneksi, tipe, tanggal)

                    tipe_file_laporan = "Sales" if tipe == "sales" else "Inventory"

                    if mode.satu_file == "ya" and data is not None:
                        nonlocal df_satufile
                        df_satufile = pd.concat([df_satufile, data], ignore_index=True)
                    else:
                        path = simpan_csv(
                            data,
                            f"AtmosID_{tipe_file_laporan}_{parse(tanggal).strftime('%Y%m%d')}.csv",
                            folder_output,
                        )
                        csv_terbentuk.append(path)

            proses_tanggal()

        if mode.satu_file == "ya" and not df_satufile.empty:
            path = simpan_csv(
                df_satufile,
                f"AtmosID_{tipe}_{parse(max(mode.tanggal)).strftime('%Y%m%d')}.csv",
                folder_output,
            )
            csv_terbentuk.append(path)

    return csv_terbentuk
