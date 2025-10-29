#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, time, json, getpass, gc, requests
from utils.color import *
from Menu.bot_captcha import run_bot
from Menu.ocr_settings import ocr_settings_menu
from Menu.ocr_accuracy import check_ocr_accuracy
from Menu.apikey_request import request_apikey
from Menu.apikey_validate import validate_captcha_key, validate_ocr_key
from Session.login import perform_login_prompt, logout_user, is_session_valid
from utils.encryptor import encrypt_file, load_referral_code
from utils.path import APIKEY_DIR, ENC_APIKEY, REFERRAL_FILE, sensitive_tmp
from Menu.info_user import show_user_info

# ======================================================
REFERRAL_DECRYPT_PASSWORD = "260805"
BASE_URL = "https://captchamoney.id"

# ======================================================
def cleanup_tmp():
    gc.collect()
    for f in list(set(sensitive_tmp)):
        try:
            if os.path.exists(f):
                os.chmod(f, 0o777)
                os.remove(f)
        except:
            pass
    sensitive_tmp.clear()

# ======================================================
def loading_bar(text="Memproses", durasi=2):
    length = 25
    for i in range(length + 1):
        bar = "█" * i + "-" * (length - i)
        percent = int((i / length) * 100)
        sys.stdout.write(f"\r{cyan(text)} [{hijau(bar)}] {percent}%")
        sys.stdout.flush()
        time.sleep(durasi / length)
    print()

# ======================================================
def input_new_apikey(password_cache=None):
    clear(); header()
    print(cyan("=== MAENU API KEY===\n"))
    print("1. Masukkan API Key Captcha")
    print("2. Masukkan API Key OCR")
    print("3. Kembali\n")
    c = input("Pilih: ").strip()

    if c == "1":
        plain_tmp = os.path.join(APIKEY_DIR, "Apikey.txt.tmp")
        enc_path = ENC_APIKEY
        tipe = "Captcha"
        validate = validate_captcha_key
        need_relogin = True
    elif c == "2":
        plain_tmp = os.path.join(APIKEY_DIR, "Apikey_OCR.tmp")
        enc_path = os.path.join(APIKEY_DIR, "Apikey_OCR")
        tipe = "OCR"
        validate = validate_ocr_key
        need_relogin = False
    else:
        return

    new_key = input(f"Masukkan API Key {tipe}: ").strip()
    if not new_key:
        print(merah("❌ API key tidak boleh kosong.")); time.sleep(1); return

    print(kuning("🔍 Mengecek validitas..."))
    valid = validate(new_key)
    if not valid:
        print(merah("❌ API Key tidak valid!"))
        input("\nTekan Enter untuk kembali..."); return

    os.makedirs(APIKEY_DIR, exist_ok=True)
    with open(plain_tmp, "w", encoding="utf-8") as f:
        f.write(new_key)
    os.chmod(plain_tmp, 0o600)

    if tipe == "OCR":
        os.replace(plain_tmp, enc_path)
        os.chmod(enc_path, 0o600)
        print(hijau(f"\n✅ API Key OCR berhasil diperbarui (tanpa enkripsi)."))
    else:
        enc_tmp = enc_path + ".tmp"
        encrypt_file(plain_tmp, enc_tmp, password_cache or getpass.getpass("Masukkan password enkripsi: ").strip())
        os.replace(enc_tmp, enc_path)
        os.chmod(enc_tmp, 0o400)
        print(hijau(f"\n✅ API Key {tipe} berhasil diperbarui dan terenkripsi ulang."))

    if need_relogin:
        logout_user()
        session = requests.Session()
        perform_login_prompt(session)

# ======================================================
def ensure_valid_session(session):
    print(kuning("🔐 Mengecek sesi login..."))
    loading_bar("Memverifikasi", 2)
    if not is_session_valid(session):
        print(kuning("\n⚠️  Sesi tidak valid, login ulang..."))
        if perform_login_prompt(session):
            print(hijau("\n✅ Login ulang berhasil!"))
            return True
        else:
            print(merah("❌ Gagal login ulang."))
            return False
    return True

# ======================================================
def ensure_referral(session):
    """Pastikan user sudah punya referral, jika belum klaim otomatis"""
    try:
        res = session.get(f"{BASE_URL}/api/userinfo.php", timeout=10)
        if res.status_code != 200:
            return False

        data = res.json()
        if data.get("referred_by"):
            return True

        if not os.path.exists(REFERRAL_FILE):
            return False

        referral_code = load_referral_code(REFERRAL_FILE, REFERRAL_DECRYPT_PASSWORD)
        payload = {"action": "claim_referral", "referral_code": referral_code}
        post = session.post(f"{BASE_URL}/api/userinfo.php", data=payload, timeout=10)
        if post.status_code == 200 and "success" in post.text.lower():
            return True
        return False
    except:
        return False

# ======================================================
session = requests.Session()

def menu():
    global session
    while True:
        clear(); header()
        print(cyan("╔══════════════════════════════════════════════╗"))
        print(cyan("║              MENU CAPTCHAMONEY          ║"))
        print(cyan("╠══════════════════════════════════════════════╣"))
        print("║ 1. Informasi Profil                          ║")
        print("║ 2. Mulai Bot Captcha                         ║")
        print("║ 3. Cek Akurasi OCR                           ║")
        print("║ 4. Pengaturan OCR                            ║")
        print("║ 5. Ganti Akun                                ║")
        print("║ 6. Minta API Key Baru                        ║")
        print("║ 7. Masukkan API Key Baru                     ║")
        print("║ 8. Keluar                                    ║")
        print(cyan("╚══════════════════════════════════════════════╝"))
        c = input("\nPilih menu: ").strip()

        if c == "1":
            if ensure_valid_session(session):
                show_user_info(session)
        elif c == "2":
            if ensure_valid_session(session):
                run_bot(session)
        elif c == "3":
            if ensure_valid_session(session):
                check_ocr_accuracy(session)
        elif c == "4":
            if ensure_valid_session(session):
                ocr_settings_menu(session)
        elif c == "5":
            clear(); header()
            print(cyan("=== GANTI AKUN ===\n"))
            print("1. Login ke akun yang sudah ada")
            print("2. Daftar akun baru")
            print("3. Kembali\n")
            sub = input("Pilih: ").strip()

            if sub == "1":
                logout_user()
                session = requests.Session()
                perform_login_prompt(session)
                ensure_referral(session)
            elif sub == "2":
                logout_user()
                session = requests.Session()
                from Session.register import perform_register_prompt
                perform_register_prompt(session)
                ensure_referral(session)
            elif sub == "3":
                continue
            else:
                print(merah("❌ Pilihan tidak valid!"))
                time.sleep(1)
        elif c == "6":
            if ensure_valid_session(session):
                request_apikey()
        elif c == "7":
            input_new_apikey()
        elif c == "8":
            cleanup_tmp()
            clear()
            print(hijau("Jangan Cepu Ya bre"))
            time.sleep(1)
            sys.exit(0)
        else:
            print(merah("❌ Pilihan tidak valid!"))
            time.sleep(1)

# ======================================================
if __name__ == "__main__":
    try:
        os.system("termux-wake-lock")
    except:
        pass

    session = requests.Session()
    clear(); header()
    loading_bar("✨ Memeriksa status sesi", 2)

    from Session.register import perform_register_prompt

    # Deteksi login pertama kali
    if not is_session_valid(session):
        clear(); header()
        print(cyan("╔══════════════════════════════════════════════╗"))
        print(cyan("║        SELAMAT DATANG DI CAPTCHA BOT         ║"))
        print(cyan("╠══════════════════════════════════════════════╣"))
        print("║ 1. Login ke akun yang sudah ada              ║")
        print("║ 2. Daftar akun baru                          ║")
        print("║ 3. Keluar                                    ║")
        print(cyan("╚══════════════════════════════════════════════╝"))
        pilihan = input("\nPilih: ").strip()
        sukses = False

        if pilihan == "1":
            sukses = perform_login_prompt(session)
        elif pilihan == "2":
            sukses = perform_register_prompt(session)
        elif pilihan == "3":
            clear()
            print(kuning("Keluar dari program..."))
            time.sleep(1)
            sys.exit(0)
        else:
            print(merah("❌ Pilihan tidak valid."))
            time.sleep(1)
            sys.exit(0)

        if not sukses:
            print(merah("\n❌ Gagal masuk. Silakan jalankan ulang script dan login kembali."))
            time.sleep(2)
            sys.exit(0)

        ensure_referral(session)
    else:
        ensure_referral(session)

    loading_bar("✨ Memuat menu utama", 2)
    menu()