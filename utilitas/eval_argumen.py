from utilitas.logging import log_dan_waktu
from dataclasses import dataclass
from argparse import Namespace
from datetime import datetime, timedelta


@dataclass
class ModeScript:
    tipe_laporan: list[str]
    tanggal: list[str]


def akhir_minggu_sebelumnya(tanggal: datetime, hari_pertama: int) -> datetime:
    tanggal_weekday = tanggal.weekday()  # 0=Senin, 6=Minggu
    selisih_hari = (tanggal_weekday - hari_pertama) % 7
    return tanggal - timedelta(days=selisih_hari + 1)


@log_dan_waktu("Mengkonversi argumen ke mode skrip")
def eval_argumen(argumen: Namespace) -> ModeScript:
    list_tipe_laporan: list[str] = (
        ["sales", "inventory"]
        if argumen.tipe_laporan == "semua"
        else [argumen.tipe_laporan]
    )

    list_tanggal: list[str] = []
    match argumen.mode_tanggal:
        case "periode":
            # unpack argumen.periode
            tanggal_awal, tanggal_akhir = (
                argumen.periode[0],
                argumen.periode[1],
            )
            # buat set tanggal antara tanggal_awal dan tanggal_akhir
            set_tanggal = set()
            # clone tanggal_awal dan while loop pada tanggal_sekarang
            tanggal_sekarang = tanggal_awal
            while tanggal_sekarang <= tanggal_akhir:
                akhir_minggu = akhir_minggu_sebelumnya(
                    tanggal_sekarang, argumen.hari_pertama
                )
                # hanya tambahkan akhir minggu ke dalam set jika lebih besar
                # atau sama dengan tanggal_awal
                if akhir_minggu >= tanggal_awal:
                    # format akhir_minggu ke dalam string kueri
                    # dan tambahkan ke dalam set
                    set_tanggal.add(akhir_minggu.strftime("%Y-%m-%d"))
                tanggal_sekarang += timedelta(days=1)
            # convert it into list and sort it
            list_tanggal = sorted(set_tanggal)
        case "tanggal":
            akhir_minggu = akhir_minggu_sebelumnya(
                argumen.tanggal, argumen.hari_pertama
            )
            list_tanggal.append(akhir_minggu.strftime("%Y-%m-%d"))

    return ModeScript(list_tipe_laporan, list_tanggal)
