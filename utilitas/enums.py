from enum import StrEnum


class TIPE_LAPORAN(StrEnum):
    SALES = "sales"
    INVENTORY = "inventory"
    SEMUA = "semua"


class MODE_TANGGAL(StrEnum):
    TANGGAL = "tanggal"
    PERIODE = "periode"


class ARGUMEN(StrEnum):
    YA = "ya"
    TIDAK = "tidak"
