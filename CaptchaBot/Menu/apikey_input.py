import os, getpass
from utils.color import *
from secure_file import encrypt_file

APIKEY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Apikey")
ENC_APIKEY = os.path.join(APIKEY_DIR, "Apikey.enc")
ENC_OCR = os.path.join(APIKEY_DIR, "Apikey_OCR.enc")

def input_apikey_manual():
    os.system("clear")
    print(cyan("=== MASUKKAN API KEY BARU (MANUAL) ===\n"))
    print("1. Masukkan API Key Captcha")
    print("2. Masukkan API Key OCR")
    print("3. Kembali\n")

    c = input("Pilih: ").strip()
    if c == "1":
        enc_path, tipe = ENC_APIKEY, "Captcha"
    elif c == "2":
        enc_path, tipe = ENC_OCR, "OCR"
    else:
        return

    new_key = input(f"Masukkan API Key {tipe}: ").strip()
    if not new_key:
        print(merah("❌ Tidak boleh kosong.")); input(); return

    pw = getpass.getpass("Masukkan password enkripsi: ").strip()
    if not pw:
        print(merah("❌ Password kosong.")); input(); return

    tmp = os.path.join(APIKEY_DIR, f"{tipe.lower()}_tmp.txt")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new_key)

    try:
        encrypt_file(tmp, enc_path, pw)
        os.remove(tmp)
        print(hijau(f"✅ API Key {tipe} berhasil disimpan."))
    except Exception as e:
        print(merah(f"❌ Gagal menyimpan: {e}"))
    input("\nTekan Enter untuk kembali...")