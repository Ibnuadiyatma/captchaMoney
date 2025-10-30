import requests, time, os, sys
from utils.color import *
from Session.login import perform_login_prompt

BASE_URL = "https://captchamoney.id"

def perform_register_prompt(session):
    """Daftarkan akun baru melalui terminal"""
    clear()
    header()
    print(cyan("=== DAFTAR AKUN BARU ===\n"))

    try:
        nama = input("Nama lengkap     : ").strip()
        email = input("Email aktif       : ").strip()
        password = input("Password          : ").strip()
        confirm = input("Ulangi password   : ").strip()

        # ✅ Validasi input kosong
        if not nama or not email or not password or not confirm:
            print(merah("\n❌ Semua kolom wajib diisi."))
            time.sleep(1.5)
            return False

        # ✅ Validasi password tidak sama
        if password != confirm:
            print(merah("\n❌ Password tidak sama."))
            time.sleep(1.5)
            return False

        clear()
        print(kuning("🕓 Mengirim data pendaftaran..."))

        payload = {
            "action": "register",
            "nama_lengkap": nama,
            "email": email,
            "password": password
        }

        url = f"{BASE_URL}/api/register.php"
        res = session.post(url, data=payload, timeout=15)

        if res.status_code != 200:
            print(merah(f"\n❌ Server tidak merespons ({res.status_code})"))
            time.sleep(1.5)
            return False

        try:
            data = res.json()
        except:
            print(merah("\n❌ Gagal membaca respons server."))
            time.sleep(1.5)
            return False

        # ✅ Hanya lanjut jika status success
        if data.get("status") == "success":
            print(hijau("\n✅ Pendaftaran berhasil!"))
            print(kuning("🔐 Melakukan login otomatis...\n"))
            time.sleep(2)
            if perform_login_prompt(session):
                return True
            else:
                print(merah("❌ Gagal login otomatis. Silakan login manual."))
                return False
        else:
            pesan = data.get("message") or data.get("msg") or "Gagal daftar akun."
            print(merah(f"\n❌ {pesan}"))
            time.sleep(2)
            return False

    except KeyboardInterrupt:
        print(merah("\n\n❌ Pendaftaran dibatalkan oleh user."))
        return False
    except Exception as e:
        print(merah(f"\n❌ Terjadi kesalahan: {e}"))
        time.sleep(2)
        return False