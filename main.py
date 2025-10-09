import logging
from dateutil.parser import parse
from utilitas.cli_parse import parse_argumen
from utilitas.eval_argumen import eval_argumen
from utilitas.rahasia import Rahasia
from utilitas.laporan import generate
from utilitas.isi_email import generate_isi_email
from utilitas.email import kirim_email

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

    file_csv = generate(mode_skrip, rahasia.db)

    if mode_skrip.kirim_email == "ya":
        # Ambil tanggal paling akhir dari mode_skrip.tanggal
        tgl_akhir = max(parse(tgl) for tgl in mode_skrip.tanggal)
        tgl_akhir_string = tgl_akhir.strftime("%Y%m%d")

        # Subyek email
        subyek_email = f"Laporan PUMA Week Ending {tgl_akhir_string}"

        isi_html = generate_isi_email(
            FILE_LOG,
            tgl_akhir_string,
            proses_sukses=bool(file_csv and len(file_csv) > 0),
        )

        kirim_email(
            gmail_account=rahasia.email.username,
            gmail_app_password=rahasia.email.password,
            subyek=subyek_email,
            to_addr=rahasia.email.to,
            isi_html=isi_html,
            lampiran=file_csv,
        )
