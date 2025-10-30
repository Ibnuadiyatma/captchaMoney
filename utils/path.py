#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# ======================================================
# 📁 Direktori utama penyimpanan file sensitif
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APIKEY_DIR = os.path.join(BASE_DIR, "Apikey")

# Buat folder Apikey jika belum ada
if not os.path.exists(APIKEY_DIR):
    os.makedirs(APIKEY_DIR, exist_ok=True)

# ======================================================
# 🔐 Path file enkripsi
# Semua file kunci dan data sensitif disimpan di folder Apikey
ENC_APIKEY = os.path.join(APIKEY_DIR, "Apikey.enc")
ENC_OCR = os.path.join(APIKEY_DIR, "Apikey_OCR.enc")

# 🔹 File referral terenkripsi
# (Digunakan oleh fitur auto-referral di main.py)
REFERRAL_FILE = os.path.join(APIKEY_DIR, "referral.json.enc")

# ======================================================
# 🧹 Daftar file sementara yang sensitif
# (Akan dibersihkan otomatis oleh cleanup_tmp() di main.py)
sensitive_tmp = []

# ======================================================
# ✅ Catatan:
# File ini digunakan untuk menentukan semua lokasi file sensitif.
# Jangan ubah nama file sembarangan, agar fungsi enkripsi/dekripsi tetap konsisten.