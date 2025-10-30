import os
import webbrowser
from utils.color import *

def request_apikey():
    clear()
    header()
    print(cyan("=== MINTA API KEY ===\n"))
    print("1. Minta API Key CaptchaMoney")
    print("2. Minta API Key OCR")
    print("3. Kembali\n")

    pilihan = input("Pilih: ").strip()

    whatsapp_number = "6282118350291"  # 🔧 ganti dengan nomor admin kamu (tanpa + atau 0 di depan)

    if pilihan == "1":
        pesan = "Halo admin, saya ingin meminta API key CaptchaMoney saya."
    elif pilihan == "2":
        pesan = "Halo admin, saya ingin meminta API key OCR saya."
    elif pilihan == "3":
        return
    else:
        print(merah("❌ Pilihan tidak valid."))
        input("\nTekan Enter untuk kembali...")
        return

    url = f"https://wa.me/{whatsapp_number}?text={pesan.replace(' ', '%20')}"
    print(f"{hijau('Jika tidak terbuka otomatis, buka manual di link berikut:')}\n{url}\n")

    try:
        # Buka langsung di Termux (Android)
        os.system(f"termux-open-url '{url}'")
    except:
        pass

    try:
        # Cadangan buka di browser default
        webbrowser.open(url)
    except:
        print(kuning("⚠️ Tidak bisa membuka browser otomatis."))

    input(hijau("\nTekan Enter untuk kembali ke menu utama..."))