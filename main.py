import logging
from utilitas.cli_parse import parse_argumen
from utilitas.eval_argumen import eval_argumen
from utilitas.rahasia import Rahasia
from utilitas.laporan import generate

FILE_LOG = "log_aplikasi.log"

# Buat root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Handler untuk menulis ke FILE_LOG
handler_file = logging.FileHandler(FILE_LOG, mode="w")
handler_file.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(handler_file)

# Handler untuk menulis ke console
handler_konsol = logging.StreamHandler()
handler_konsol.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
logger.addHandler(handler_konsol)

if __name__ == "__main__":
    argumen = parse_argumen()
    mode_skrip = eval_argumen(argumen)
    rahasia = Rahasia()
    generate(mode_skrip, rahasia.db)
