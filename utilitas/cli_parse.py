import argparse
from datetime import datetime
from dateutil.parser import parse

def parser_tanggal(tanggal_str: str) -> str:
    try:
        return parse(tanggal_str).strftime("%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Tanggal tidak valid: {tanggal_str}")

def parse_argumen() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Command line interface untuk automasi laporan mingguan PUMA")
    parser.add_argument(
        "-tl",
        "--tipe-laporan",
        choices=["sales", "inventory", "semua"],
        default="semua",
        help="Tipe laporan yang akan dihasilkan (default: semua)"
    )
    parser.add_argument(
        "-p",
        "--periode",
        type=parser_tanggal,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Periode laporan dalam format tanggal YYYY-MM-DD, YYYYMMDD, dll (default: hari ini)"
    )
    return parser.parse_args()