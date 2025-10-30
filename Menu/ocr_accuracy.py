#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import base64
import requests
from PIL import Image, ImageEnhance, ImageFilter
from Menu.ocr_settings import load_ocr_settings

# ======================================================
BASE_URL = "https://captchamoney.id/api"
CAPTCHA_ENDPOINT = f"{BASE_URL}/captcha_generate.php"
TIMEOUT = 10
# ======================================================

# Warna
def warna(teks, kode): return f"\033[{kode}m{teks}\033[0m"
def hijau(teks): return warna(teks, "92")
def merah(teks): return warna(teks, "91")
def kuning(teks): return warna(teks, "93")
def cyan(teks): return warna(teks, "96")
def clear(): os.system("clear" if os.name == "posix" else "cls")

# ======================================================
def check_ocr_accuracy(session):
    clear()
    print(cyan("╔════════════════════════════════════╗"))
    print(cyan("║       🔍  CEK AKURASI OCR          ║"))
    print(cyan("╚════════════════════════════════════╝\n"))

    settings = load_ocr_settings()
    print(kuning("Pengaturan OCR saat ini:"))
    for k, v in settings.items():
        print(f"  {hijau(k.capitalize())}: {v}")
    print()

    print(cyan("Mengambil captcha...\n"))

    try:
        # 🔹 Ambil captcha dari server
        r = session.get(CAPTCHA_ENDPOINT, timeout=TIMEOUT)
        j = r.json()
        img_field = j.get("image")
        if not img_field:
            print(merah("❌ Tidak ada field image di respon server."))
            input("\nTekan Enter untuk kembali...")
            return

        img_bytes = base64.b64decode(img_field.split(",")[-1])

        # 🔹 Pastikan folder di penyimpanan internal ada
        save_dir = "/storage/emulated/0/CaptchaBot/"
        os.makedirs(save_dir, exist_ok=True)

        img_path = os.path.join(save_dir, "captcha_sample.png")
        processed_path = os.path.join(save_dir, "captcha_processed.png")

        # 🔹 Hapus file lama jika ada
        for f in [img_path, processed_path]:
            if os.path.exists(f):
                try:
                    os.remove(f)
                    print(kuning(f"🧹 Menghapus file lama: {os.path.basename(f)}"))
                except Exception as e:
                    print(merah(f"❌ Gagal menghapus {f}: {e}"))

        # 🔹 Simpan file captcha asli baru
        with open(img_path, "wb") as f:
            f.write(img_bytes)

        # 🔹 Terapkan filter OCR dari pengaturan
        img = Image.open(img_path).convert("RGB")
        img = ImageEnhance.Contrast(img).enhance(settings["contrast"])
        img = ImageEnhance.Brightness(img).enhance(settings["brightness"])
        if settings.get("sharpen", True):
            img = img.filter(ImageFilter.SHARPEN)
        img.save(processed_path)

        # 🔹 Scan media agar muncul di galeri Android
        os.system(f'termux-media-scan "{save_dir}"')

        print(hijau("\n✅ Captcha contoh berhasil disimpan di penyimpanan internal."))
        print(cyan(f"\n• File Asli     : {img_path}"))
        print(cyan(f"• File Hasil    : {processed_path}\n"))
        print(kuning("Silakan buka folder 'CaptchaBot' di penyimpanan internal.\n"))

    except Exception as e:
        print(merah(f"❌ Gagal ambil captcha: {e}"))

    input("\nTekan Enter untuk kembali...")