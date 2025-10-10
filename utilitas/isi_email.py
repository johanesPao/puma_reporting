from pathlib import Path
import html
import re


def generate_isi_email(
    path_file_log: str,
    week_ending_str: str,
    proses_kirim_sftp_sukses: bool | None,
    proses_generate_sukses: bool,
) -> str:
    isi_html = f"""
    <p>Dear all,</p>

    <p>Laporan mingguan <i>sales</i> dan <i>inventory</i> PUMA untuk <i>week ending date</i> 
    {week_ending_str} 
    {
        "berhasil di-<i>generate</i>"
        if proses_generate_sukses
        else "<span style='color:#ff5555;'>gagal di-<i>generate</i></span>."
    }
    {
        ", namun file gagal dikirimkan ke SFTP PUMA."
        if not proses_kirim_sftp_sukses
        else "dan dikirimkan ke SFTP PUMA."
    }</p> 
    {
        "<p><i>Intervensi manual dengan SSH atau RDP ke server perlu dilakukan untuk menjalankan ulang skrip."
        if not proses_generate_sukses or not proses_kirim_sftp_sukses
        else ""
    }
    <p>Log dari proses adalah sebagai berikut.</p>

    <div style="background-color:#f9f9f9;border:1px solid #ddd;padding:12px;border-radius:8px;
    font-family:Consolas,Menlo,monospace;font-size:13px;line-height:1.5;white-space:pre-wrap;">
    """

    if Path(path_file_log).exists():
        with open(path_file_log, "r", encoding="utf-8") as file_log:
            for baris in file_log:
                if not baris.strip():
                    continue

                baris_aman = html.escape(baris.strip())

                # Warnai timestamp
                baris_aman = re.sub(
                    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})",
                    r"<span style='color:#9ca3af;'>\1</span>",
                    baris_aman,
                )

                # Warnai level log
                baris_aman = baris_aman.replace(
                    "[INFO]", "<span style='color:#6b7280;'>[INFO]</span>"
                ).replace("[ERROR]", "<span style='color:#b91c1c;'>[ERROR]</span>")

                # Color-coding berdasar konten log
                if "❌" in baris_aman:
                    warna = "#b91c1c"  # merah
                elif "✅" in baris_aman:
                    warna = "#166534"  # hijau
                elif "▶️" in baris_aman:
                    warna = "#1d4ed8"  # biru
                else:
                    warna = "#374151"  # abu-abu gelap

                isi_html += f"<pre style='margin:0;color:{warna};'><code>{baris_aman}</code></pre>"

        isi_html += "</div>"
    else:
        isi_html += "<p><b>⚠️ File log tidak ditemukan.</b></p></div>"

    isi_html += "<p>Regards,<br>Pao</p>"

    return isi_html
