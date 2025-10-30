import requests
from utils.color import *

# ==============================
# Base URL CaptchaMoney
BASE_URL = "https://captchamoney.id/api"

def validate_captcha_key(api_key: str) -> bool:
    """Validasi API Key CaptchaMoney."""
    try:
        if not api_key.strip():
            print(merah("❌ API Key kosong."))
            return False

        payload = {"apikey": api_key}
        res = requests.post(f"{BASE_URL}/userinfo.php", data=payload, timeout=10)

        if res.status_code != 200:
            print(merah(f"❌ Server gagal merespons ({res.status_code})"))
            return False

        try:
            data = res.json()
        except:
            print(merah("❌ Gagal membaca respons server."))
            return False

        if data.get("status") == "success" or data.get("email"):
            print(hijau("✅ API Key CaptchaMoney valid."))
            return True
        else:
            print(merah("❌ API Key CaptchaMoney tidak dikenali server."))
            return False
    except Exception as e:
        print(merah(f"❌ Kesalahan validasi CaptchaMoney: {e}"))
        return False


def validate_ocr_key(api_key: str) -> bool:
    """Validasi API Key OCR.Space."""
    try:
        if not api_key.strip():
            print(merah("❌ API Key kosong."))
            return False

        url = "https://api.ocr.space/parse/image"
        data = {
            "apikey": api_key,
            "isOverlayRequired": False,
            "OCREngine": 2
        }

        # Tes kecil tanpa gambar (OCR.Space akan balas error JSON spesifik kalau key valid)
        res = requests.post(url, data=data, timeout=10)

        if res.status_code != 200:
            print(merah(f"❌ OCR.Space gagal merespons ({res.status_code})"))
            return False

        try:
            j = res.json()
        except:
            print(merah("❌ Gagal membaca respons OCR.Space"))
            return False

        # OCR.Space akan tetap mengembalikan 'OCRExitCode' walau tanpa file jika key valid
        if "OCRExitCode" in j or j.get("IsErroredOnProcessing") is not None:
            print(hijau("✅ API Key OCR.Space valid."))
            return True
        else:
            print(merah("❌ API Key OCR.Space tidak dikenali."))
            return False

    except Exception as e:
        print(merah(f"❌ Kesalahan validasi OCR.Space: {e}"))
        return False