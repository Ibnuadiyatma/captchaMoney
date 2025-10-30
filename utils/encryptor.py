#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, base64, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# ======================================================
# 🧩 Fungsi dasar enkripsi & dekripsi AES-256 (CBC)
# ======================================================

def _derive_key(password: str) -> bytes:
    """Turunkan key 32 byte dari password (SHA256)."""
    return hashlib.sha256(password.encode("utf-8")).digest()


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    """Enkripsi file input_path → output_path (AES-256-CBC)."""
    key = _derive_key(password)
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(input_path, "rb") as f_in:
        plaintext = f_in.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_path, "wb") as f_out:
        f_out.write(iv + ciphertext)


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    """Dekripsi file terenkripsi → simpan ke output_path."""
    key = _derive_key(password)
    with open(input_path, "rb") as f_in:
        data = f_in.read()
    iv, ciphertext = data[:16], data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    with open(output_path, "wb") as f_out:
        f_out.write(plaintext)

# ======================================================
# 🔹 Helper opsional: load_referral_code()
# ======================================================

def load_referral_code(enc_path: str, password: str) -> str:
    """
    Dekripsi file referral terenkripsi & kembalikan kode referral sebagai string.
    Digunakan oleh main.py saat auto-referral.
    """
    import json, tempfile
    if not os.path.exists(enc_path):
        raise FileNotFoundError(f"File tidak ditemukan: {enc_path}")

    tmp_plain = tempfile.NamedTemporaryFile(delete=False).name
    decrypt_file(enc_path, tmp_plain, password)

    try:
        with open(tmp_plain, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        with open(tmp_plain, "r", encoding="utf-8") as f:
            data = f.read().strip()
    finally:
        try: os.remove(tmp_plain)
        except: pass

    if isinstance(data, dict):
        for k in ("referral", "referral_code", "code"):
            if k in data:
                return str(data[k]).strip()
        if len(data) == 1:
            return str(next(iter(data.values()))).strip()
    elif isinstance(data, str):
        return data.strip()
    raise ValueError("Format referral.json.enc tidak valid atau kosong.")

# ======================================================
# ✅ Catatan:
#  - AES-256-CBC digunakan dengan IV acak (aman untuk file kecil & API key).
#  - File terenkripsi bisa didekripsi di mana saja selama password sama.
#  - load_referral_code() dipakai otomatis oleh ensure_referral() di main.py.
# ======================================================