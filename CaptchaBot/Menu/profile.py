# Menu/profile.py
import requests
import json
import time
from utils.color import *

USERINFO_ENDPOINT = "https://captchamoney.id/api/userinfo.php"

def show_profile(session):
    clear()
    print(cyan("=== INFORMASI PROFIL ===\n"))
    try:
        r = session.get(USERINFO_ENDPOINT, timeout=10)
        if r.status_code != 200:
            print(merah("❌ Gagal mengambil data profil dari server."))
            input("\nTekan Enter untuk kembali...")
            return

        data = r.json()
        if data.get("status") != "success":
            print(merah(f"❌ Gagal: {data.get('message', 'Tidak diketahui')}"))
            input("\nTekan Enter untuk kembali...")
            return

        # Format tampilan yang lebih rapih
        print(hijau("Status Akun  :"), data.get("user_status", "-"))
        print(hijau("Nama Lengkap :"), data.get("nama_lengkap", "-"))
        print(hijau("Email        :"), data.get("email", "-"))
        print(hijau("Level        :"), data.get("level", "-"))
        print(hijau("Referral Code:"), data.get("referral_code", "-"))
        print(hijau("Referred By  :"), data.get("referred_by", "-"))
        print(hijau("Points       :"), data.get("points", "0"))
        print(hijau("Kupon   :"), data.get("kupon_saya", "0"))
        print(hijau("Total Scratch:"), data.get("total_scratch", "0"))
        print(hijau("Total Referral:"), data.get("total_referral", "0"))
        print(hijau("Admin        :"), "✅ Ya" if data.get("is_admin") == "1" else "❌ Tidak")

    except requests.exceptions.Timeout:
        print(merah("⏰ Timeout saat mengambil data profil."))
    except json.JSONDecodeError:
        print(merah("❌ Respons server tidak valid (bukan JSON)."))
    except Exception as e:
        print(merah(f"❌ Terjadi kesalahan: {e}"))

    # Tambahkan jeda agar tidak langsung hilang
    print("\n" + abu("───────────────────────────────"))
    input(hijau("Tekan Enter untuk kembali ke menu..."))