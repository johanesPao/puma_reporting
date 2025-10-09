from utilitas.logging import log_dan_waktu
from dataclasses import dataclass
from argparse import Namespace
from datetime import datetime, timedelta
from utilitas.enums import TIPE_LAPORAN, MODE_TANGGAL, ARGUMEN


@dataclass
class ModeScript:
    tipe_laporan: list[str]
    tanggal: list[str]
    satu_file: bool
    kirim_email: bool
    transfer_sftp: bool


def akhir_minggu_sebelumnya(tanggal: datetime, hari_pertama: int) -> datetime:
    tanggal_weekday = tanggal.weekday()  # 0=Senin, 6=Minggu
    selisih_hari = (tanggal_weekday - hari_pertama) % 7
    return tanggal - timedelta(days=selisih_hari + 1)


@log_dan_waktu("Mengkonversi argumen ke mode skrip")
def eval_argumen(argumen: Namespace) -> ModeScript:
    list_tipe_laporan: list[str] = (
        [TIPE_LAPORAN.SALES, TIPE_LAPORAN.INVENTORY]
        if argumen.tipe_laporan == TIPE_LAPORAN.SEMUA
        else [argumen.tipe_laporan]
    )

    list_tanggal: list[str] = []
    match argumen.mode_tanggal:
        case MODE_TANGGAL.PERIODE:
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
        case MODE_TANGGAL.TANGGAL:
            akhir_minggu = akhir_minggu_sebelumnya(
                argumen.tanggal, argumen.hari_pertama
            )
            list_tanggal.append(akhir_minggu.strftime("%Y-%m-%d"))

    return ModeScript(
        list_tipe_laporan,
        list_tanggal,
        argumen.satu_file == ARGUMEN.YA,
        argumen.kirim_email == ARGUMEN.YA,
        argumen.transfer_sftp == ARGUMEN.YA,
    )
