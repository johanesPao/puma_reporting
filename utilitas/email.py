import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path


def kirim_email(
    gmail_account: str,
    gmail_app_password: str,
    subyek: str,
    to_addr: str,
    isi_html: str,
    lampiran: list[str] | None = None,
    cc_addr: str | None = None,
) -> None:
    dari = gmail_account
    password = gmail_app_password

    pesan = MIMEMultipart()
    pesan["From"] = dari
    pesan["To"] = to_addr
    pesan["Subject"] = subyek

    # Tambahkan CC
    if cc_addr:
        pesan["Cc"] = cc_addr

    # HTML body email
    pesan.attach(MIMEText(isi_html, "html", "utf-8"))

    # Lampiran
    if lampiran:
        for file_path in lampiran:
            path = Path(file_path)
            if not path.exists():
                print(f"⚠️ File tidak ditemukan: {file_path}")
                continue

            with open(path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f'attachment; filename="{path.name}"'
                )
                pesan.attach(part)

    # Penerima dan Carbon Copy
    penerima = [to_addr]
    if cc_addr:
        penerima.extend(cc_addr)

    # Kirim
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(dari, password)
        server.send_message(dari, penerima, pesan.as_string())
