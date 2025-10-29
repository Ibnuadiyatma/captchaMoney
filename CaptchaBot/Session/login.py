#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, requests, time
from requests.utils import dict_from_cookiejar, cookiejar_from_dict

# ======================================================
BASE_URL = "https://captchamoney.id/api"
CAPTCHA_ENDPOINT = f"{BASE_URL}/captcha_generate.php"
LOGIN_ENDPOINT = f"{BASE_URL}/login.php"
USERINFO_ENDPOINT = f"{BASE_URL}/userinfo.php"

COOKIES_FILE = "cookies.json"
USER_FILE = "user.json"
TIMEOUT = 10

# ======================================================
# 🔐 Simpan dan muat cookies
def save_cookies_to_file(session, filename=COOKIES_FILE):
    try:
        cookie_dict = dict_from_cookiejar(session.cookies)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(cookie_dict, f)
        print(f"[✅] sesi disimpan")
    except Exception as e:
        print(f"[❌] Gagal menyimpan {e}")

def load_cookies_from_file(session, filename=COOKIES_FILE):
    if not os.path.exists(filename):
        return False
    try:
        with open(filename, "r", encoding="utf-8") as f:
            cookie_dict = json.load(f)
        session.cookies = cookiejar_from_dict(cookie_dict)
        print(f"[ℹ] Cookies dimuat dari {filename}")
        return True
    except Exception as e:
        print(f"[❌] Gagal muat cookies: {e}")
        return False

# ======================================================
# 👤 Simpan dan muat user info
def save_user_creds(email, password):
    try:
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump({"email": email, "password": password}, f)
        print(f"[✅] User disimpan ke {USER_FILE}")
    except Exception as e:
        print(f"[❌] Gagal simpan user: {e}")

def load_user_creds():
    if not os.path.exists(USER_FILE):
        return None, None
    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("email"), data.get("password")
    except:
        return None, None

# ======================================================
# 🔑 Login dan cek sesi
def login(email, password, session):
    data = {"email": email, "password": password, "remember": "1", "agree": "1"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://captchamoney.id/",
    }
    print("[*] Melakukan login...")
    try:
        r = session.post(LOGIN_ENDPOINT, data=data, headers=headers, timeout=TIMEOUT)
        resp = r.json()
        if resp.get("status") == "success":
            print("[✅] Login berhasil!")
            save_cookies_to_file(session)
            return True
        else:
            print("❌ Login gagal:", resp.get("message"))
    except Exception as e:
        print("❌ Kesalahan saat login:", e)
    return False

def perform_login_prompt(session):
    email, password = load_user_creds()
    if email and password:
        print(f"[ℹ] Login otomatis sebagai {email}")
        if login(email, password, session):
            return True
        else:
            print("[⚠️] Gagal login otomatis, meminta input manual...")
    email = input("Masukkan email login: ").strip()
    password = input("Masukkan kata sandi: ").strip()
    if login(email, password, session):
        save_user_creds(email, password)
        return True
    return False

def is_session_valid(session):
    """Cek apakah sesi login masih aktif"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = session.get(USERINFO_ENDPOINT, headers=headers, timeout=TIMEOUT)
        if r.status_code != 200:
            return False
        data = r.json()
        if data.get("status") == "success":
            return True
        msg = str(data.get("message", "")).lower()
        if "login" in msg or "unauthor" in msg:
            return False
        return True
    except:
        return False

# ======================================================
# 🚪 Logout user
def logout_user():
    """Hapus cookies & data user untuk logout total."""
    try:
        if os.path.exists(COOKIES_FILE):
            os.remove(COOKIES_FILE)
            print("[🧹] Cookies dihapus.")
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
            print("[🧹] Data user dihapus.")
        print("[✅] Logout berhasil.")
    except Exception as e:
        print(f"[⚠️] Gagal logout: {e}")