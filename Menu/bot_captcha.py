#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import base64
import json
import re
import requests
from PIL import Image, ImageEnhance, ImageFilter

# ======================================================
BASE_URL = "https://captchamoney.id/api"
CAPTCHA_ENDPOINT = f"{BASE_URL}/captcha_generate.php"
SUBMIT_ENDPOINT = f"{BASE_URL}/captcha_submit.php"

COOKIES_FILE = os.path.join(os.path.dirname(__file__), "..", "cookies.json")
APIKEY_OCR_FILE = os.path.join(os.path.dirname(__file__), "..", "Apikey", "Apikey_OCR")

DELAY_BETWEEN = 3
TIMEOUT = 10
OCR_FAIL_LIMIT = 5
# ======================================================

# ======================================================
# Warna Terminal
def warna(teks, kode): return f"\033[{kode}m{teks}\033[0m"
def hijau(teks): return warna(teks, "92")
def merah(teks): return warna(teks, "91")
def kuning(teks): return warna(teks, "93")
def cyan(teks): return warna(teks, "96")
# ======================================================


# ======================================================
# UTILITAS DASAR
def load_api_key():
    if not os.path.exists(APIKEY_OCR_FILE):
        print(merah(f"❌ File {APIKEY_OCR_FILE} tidak ditemukan."))
        return None
    with open(APIKEY_OCR_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def clean_temp_files():
    for f in ["captcha.png", "captcha_preprocessed.png"]:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass
# ======================================================


# ======================================================
# CAPTCHA & OCR
def get_captcha_and_save(session):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = session.get(CAPTCHA_ENDPOINT, headers=headers, timeout=TIMEOUT)
        data = r.json()
    except Exception as e:
        print(merah(f"❌ Gagal ambil captcha: {e}"))
        return None

    img_field = data.get("image")
    if not img_field:
        print(merah("❌ Tidak ada field 'image' di response."))
        return None

    try:
        img_bytes = base64.b64decode(img_field.split(",")[-1])
        with open("captcha.png", "wb") as f:
            f.write(img_bytes)
        return "captcha.png"
    except Exception as e:
        print(merah(f"❌ Gagal simpan captcha.png: {e}"))
        return None


def preprocess_image(img_path):
    """Perbaikan kontras agar teks captcha lebih hitam dan jelas."""
    try:
        img = Image.open(img_path).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(2.5)
        img = ImageEnhance.Brightness(img).enhance(0.9)
        img = img.filter(ImageFilter.SHARPEN)
        pre_path = "captcha_preprocessed.png"
        img.save(pre_path)
        return pre_path
    except Exception as e:
        print(merah(f"❌ Gagal preprocessing gambar: {e}"))
        return img_path


def solve_with_ocr_space(image_path, api_key):
    """Gunakan OCR.Space API untuk membaca teks captcha."""
    proc_path = preprocess_image(image_path)
    url = "https://api.ocr.space/parse/image"
    try:
        with open(proc_path, "rb") as f:
            files = {"file": f}
            data = {"apikey": api_key, "language": "eng", "isOverlayRequired": False, "OCREngine": 2}
            r = requests.post(url, files=files, data=data, timeout=TIMEOUT)
        j = r.json()
        parsed = j.get("ParsedResults")
        if not parsed:
            print(merah("❌ OCR.Space tidak mengembalikan hasil."))
            return None
        raw_text = parsed[0].get("ParsedText", "")
        clean = re.sub(r"[^A-Za-z0-9]", "", raw_text).strip()
        print(cyan(f"[🔍] Hasil OCR: {raw_text.strip()} -> {hijau(clean)}"))
        return clean if clean else None
    except Exception as e:
        print(merah(f"❌ OCR gagal: {e}"))
        return None


def submit_captcha(session, text):
    if not text:
        print(merah("❌ Tidak ada teks captcha untuk dikirim."))
        return False
    try:
        data = {"captcha": text}
        r = session.post(SUBMIT_ENDPOINT, data=data, timeout=TIMEOUT)
        res = r.json()
        if res.get("status") == "success":
            print(hijau("[✅] Captcha berhasil disubmit!"))
        else:
            print(kuning(f"[⚠️] Response server: {res}"))
        return True
    except Exception as e:
        print(merah(f"❌ Gagal kirim captcha: {e}"))
        return False
# ======================================================


# ======================================================
# BOT UTAMA
def run_bot(session):
    """Mode otomatis bot captcha"""
    clear_screen()
    print(cyan("=== MODE BOT CAPTCHA ===\n"))
    api_key = load_api_key()
    if not api_key:
        input("Tekan Enter untuk kembali...")
        return

    counter = 1
    fail_count = 0
    ocr_fail = 0

    try:
        while True:
            print(cyan(f"\n=== [🤖 CAPTCHA #{counter}] ==="))
            print(kuning(f"[🕒] {time.strftime('%Y-%m-%d %H:%M:%S')}"))

            # Ambil captcha
            img_path = get_captcha_and_save(session)
            if not img_path:
                fail_count += 1
                if fail_count >= 3:
                    print(kuning("[⚠️] Gagal ambil captcha 3x, coba login ulang..."))
                    break
                time.sleep(DELAY_BETWEEN)
                continue

            # OCR solve
            text = solve_with_ocr_space(img_path, api_key)
            if not text:
                ocr_fail += 1
                print(merah(f"❌ OCR gagal membaca teks ({ocr_fail}/{OCR_FAIL_LIMIT})"))
                if ocr_fail >= OCR_FAIL_LIMIT:
                    print(kuning("\n[♻️] Gagal terlalu banyak, hentikan sementara."))
                    break
                time.sleep(DELAY_BETWEEN)
                continue

            # Submit captcha
            submit_captcha(session, text)
            clean_temp_files()
            ocr_fail = 0
            fail_count = 0
            print(hijau("[✅] Selesai satu putaran."))

            counter += 1
            time.sleep(DELAY_BETWEEN)

    except KeyboardInterrupt:
        print(merah("\n[🛑] Bot dihentikan oleh pengguna."))
        input("Tekan Enter untuk kembali ke menu...")

# ======================================================


# ======================================================
def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")