#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, requests, time
from utils.color import *
from Session.login import USERINFO_ENDPOINT, is_session_valid, perform_login_prompt

# ======================================================
def show_user_info(session):
    """Menampilkan informasi profil user dari API userinfo.php"""
    clear()
    print(cyan("=== INFORMASI AKUN ===\n"))

    # Pastikan sesi masih valid
    if not is_session_valid(session):
        print(kuning("⚠️ Sesi tidak valid, silakan login ulang."))
        if not perform_login_prompt(session):
            print(merah("❌ Gagal login ulang."))
            input("\nTekan Enter untuk kembali...")
            return

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = session.get(USERINFO_ENDPOINT, headers=headers, timeout=10)
        data = r.json()
    except Exception as e:
        print(merah(f"❌ Gagal mengambil data user: {e}"))
        input("\nTekan Enter untuk kembali...")
        return

    if not data or data.get("status") != "success":
        print(merah("❌ Gagal memuat informasi user."))
        input("\nTekan Enter untuk kembali...")
        return

    # Format tampilan info user
    print(hijau("Status akun: "), data.get("user_status", "-"))
    print(hijau("Nama lengkap: "), data.get("nama_lengkap", "-"))
    print(hijau("Email: "), data.get("email", "-"))
    print(hijau("Level: "), data.get("level", "-").capitalize())
    print(hijau("Points: "), data.get("points", "0"))
    print(hijau("Kupon saya: "), data.get("kupon_saya", "0"))
    print(hijau("Referral code: "), data.get("referral_code", "-"))
    print(hijau("Referred by: "), data.get("referred_by", "-"))
    print(hijau("Total Captcha: "), data.get("total_scratch", "0"))
    print(hijau("Total Referral: "), data.get("total_referral", "0"))
    print(hijau("Admin: "), "Ya" if data.get("is_admin") == "1" else "Tidak")

    print("\n" + abu("Succes mengambil Data"))
    input("\nTekan Enter untuk kembali...")