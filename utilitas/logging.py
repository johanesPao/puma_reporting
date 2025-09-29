import logging
import time
import functools

# list dari hasil logging
hasil_proses: list[str] = []


def log_dan_waktu(nama_proses: str):
    def decorator_log_dan_waktu(fungsi):
        @functools.wraps(fungsi)
        def wrapper(*argumen, **kw_argumen):
            logging.info(f"Memulai proses: {nama_proses}")
            waktu_mulai = time.time()
            try:
                hasil = fungsi(*argumen, **kw_argumen)
                durasi = time.time() - waktu_mulai
                pesan_sukses = f"✅ {nama_proses} selesai dalam {durasi:.2f} detik."
                logging.info(pesan_sukses)
                hasil_proses.append(pesan_sukses)
                return hasil
            except Exception as e:
                durasi = time.time() - waktu_mulai
                pesan_gagal = f"❌ {nama_proses} gagal setelah {durasi:.2f} detik | Kesalahan: {e}"
                logging.exception(pesan_gagal)
                hasil_proses.append(pesan_gagal)
                # Jangan raise error, lanjutkan proses selanjutnya
                return None

        return wrapper

    return decorator_log_dan_waktu
