#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
from utils.color import *
from Session.login import is_session_valid, perform_login_prompt

# ======================================================
OCR_SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "ocr_settings.json")
# ======================================================

# Default pengaturan OCR
default_settings = {
    "contrast": 2.5,
    "brightness": 0.9,
    "sharpen": True,
    "filter": "NONE"
}

# ======================================================
def load_ocr_settings():
    if not os.path.exists(OCR_SETTINGS_FILE):
        save_ocr_settings(default_settings)
        return default_settings
    try:
        with open(OCR_SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default_settings


def save_ocr_settings(settings):
    with open(OCR_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def preview_ocr_settings():
    settings = load_ocr_settings()
    print(cyan("=== PENGATURAN OCR SAAT INI ==="))
    for k, v in settings.items():
        print(f"{hijau(k.capitalize()):15}: {v}")
    print()

# ======================================================
def ocr_settings_menu(session):
    """
    Menampilkan menu pengaturan OCR.
    Kini menerima argumen 'session' agar konsisten dengan main.py.
    """
    # Cek sesi valid
    if not is_session_valid(session):
        print(kuning("⚠️ Sesi tidak valid, silakan login ulang..."))
        if not perform_login_prompt(session):
            print(merah("❌ Gagal login ulang."))
            input("\nTekan Enter untuk kembali...")
            return

    while True:
        clear()
        print(cyan("╔════════════════════════════════╗"))
        print(cyan("║       ⚙️  PENGATURAN OCR       ║"))
        print(cyan("╚════════════════════════════════╝\n"))

        settings = load_ocr_settings()
        for k, v in settings.items():
            print(f"{hijau(k.capitalize()):15}: {v}")

        print("\n1. Ubah Contrast")
        print("2. Ubah Brightness")
        print("3. Aktifkan/Nonaktifkan Sharpen")
        print("4. Reset ke Default")
        print("5. Kembali ke Menu Utama\n")

        pilihan = input("Pilih: ").strip()

        if pilihan == "1":
            try:
                val = float(input("Masukkan nilai contrast (1.0 - 5.0): "))
                settings["contrast"] = max(0.5, min(val, 5.0))
            except:
                print(merah("❌ Nilai tidak valid."))
        elif pilihan == "2":
            try:
                val = float(input("Masukkan nilai brightness (0.5 - 2.0): "))
                settings["brightness"] = max(0.5, min(val, 2.0))
            except:
                print(merah("❌ Nilai tidak valid."))
        elif pilihan == "3":
            settings["sharpen"] = not settings["sharpen"]
            print(kuning(f"Sharpen {'aktif' if settings['sharpen'] else 'nonaktif'}."))
        elif pilihan == "4":
            settings = default_settings.copy()
            print(hijau("✅ Pengaturan direset ke default."))
        elif pilihan == "5":
            save_ocr_settings(settings)
            print(hijau("✅ Pengaturan disimpan."))
            time.sleep(1)
            break
        else:
            print(merah("❌ Pilihan tidak valid."))

        save_ocr_settings(settings)
        input("\nTekan Enter untuk lanjut...")