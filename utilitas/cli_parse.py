import argparse
from datetime import datetime
from dateutil.parser import parse


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
        choices=["sales", "inventory", "semua"],
        default="semua",
        help="Tipe laporan yang akan dihasilkan (default: semua)",
    )
    parser.add_argument(
        "-mt",
        "--mode-tanggal",
        choices=["tanggal", "periode"],
        default="tanggal",
        help="Mode dalam menjalankan laporan (default: tanggal)",
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
    args = parser.parse_args()

    if args.mode_tanggal == "periode" and args.periode is None:
        parser.error("Mode 'periode' mengharuskan argumen --periode diisi.")

    return args
