from utilitas.logging import log_dan_waktu
import argparse
from datetime import datetime
from dateutil.parser import parse
from utilitas.enums import TIPE_LAPORAN, MODE_TANGGAL, ARGUMEN


def parser_weekday_python(hari_pertama: str) -> int:
    return int(hari_pertama) - 1


def parser_tanggal(tanggal_str: str) -> datetime:
    try:
        return parse(tanggal_str)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Tanggal tidak valid: {tanggal_str}")


def parser_periode(periode_str: str) -> tuple[datetime, datetime]:
    try:
        tanggal_mulai, tanggal_akhir = periode_str.split(",")

        if parse(tanggal_mulai) > parse(tanggal_akhir):
            raise argparse.ArgumentTypeError(
                f"Periode tidak valid: {periode_str}. "
                "Tanggal mulai tidak bisa lebih besar dari tanggal akhir."
            )

        return parser_tanggal(tanggal_mulai), parser_tanggal(tanggal_akhir)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Periode tidak valid: {periode_str}. "
            "Gunakan format YYYY-MM-DD,YYYY-MM-DD atau YYYYMMDD,YYYYMMDD."
        )


@log_dan_waktu("Membaca argumen dari command line")
def parse_argumen() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Command line interface untuk automasi laporan mingguan PUMA"
    )
    parser.add_argument(
        "-hp",
        "--hari-pertama",
        type=parser_weekday_python,
        choices=range(1, 8),
        default=0,
        help="Hari pertama dalam minggu (1=Senin, 7=Minggu) (default: 1)",
    )
    parser.add_argument(
        "-tl",
        "--tipe-laporan",
        choices=[TIPE_LAPORAN.SALES, TIPE_LAPORAN.INVENTORY, TIPE_LAPORAN.SEMUA],
        default=TIPE_LAPORAN.SEMUA,
        help=f"Tipe laporan yang akan dihasilkan (default: {TIPE_LAPORAN.SEMUA})",
    )
    parser.add_argument(
        "-mt",
        "--mode-tanggal",
        choices=[MODE_TANGGAL.TANGGAL, MODE_TANGGAL.PERIODE],
        default=MODE_TANGGAL.TANGGAL,
        help=f"Mode dalam menjalankan laporan (default: {MODE_TANGGAL.TANGGAL})",
    )
    parser.add_argument(
        "-t",
        "--tanggal",
        type=parser_tanggal,
        default=datetime.now(),
        help="Tanggal laporan dalam format tanggal YYYY-MM-DD, YYYYMMDD, dll (default: hari ini)",
    )
    parser.add_argument(
        "-p",
        "--periode",
        type=parser_periode,
        default=None,
        help="Periode laporan dalam format YYYY-MM-DD,YYYY-MM-DD atau YYYYMMDD,YYYYMMDD"
        " dimana tanggal pertama lebih kecil dari tanggal kedua (default: None)",
    )
    parser.add_argument(
        "-sf",
        "--satu-file",
        type=str,
        choices=[ARGUMEN.YA, ARGUMEN.TIDAK],
        default=ARGUMEN.TIDAK,
        help=f"Dump data laporan per tipe laporan dalam periode (default: {ARGUMEN.TIDAK})",
    )
    parser.add_argument(
        "-ke",
        "--kirim-email",
        type=str,
        choices=[ARGUMEN.YA, ARGUMEN.TIDAK],
        default=ARGUMEN.YA,
        help=f"Mengirimkan email pada akhir proses (default: {ARGUMEN.YA})",
    )
    parser.add_argument(
        "-ts",
        "--transfer-sftp",
        type=str,
        choices=[ARGUMEN.YA, ARGUMEN.TIDAK],
        default=ARGUMEN.YA,
        help=f"Transfer file hasil dump ke sftp target (default: {ARGUMEN.YA})",
    )
    args = parser.parse_args()

    if args.mode_tanggal == MODE_TANGGAL.PERIODE and args.periode is None:
        parser.error(
            f"Mode '{MODE_TANGGAL.PERIODE}' mengharuskan argumen --periode diisi."
        )

    if args.periode is not None and args.mode_tanggal == MODE_TANGGAL.TANGGAL:
        parser.error(
            f"--periode / -p tidak dapat digunakan jika -mt / --mode-tanggal tidak sama dengan {MODE_TANGGAL.PERIODE}"
        )

    return args
