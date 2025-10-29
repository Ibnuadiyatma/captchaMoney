# secure_file.py
# -----------------------------------------
# Utility untuk enkripsi / dekripsi file sensitif (AES-GCM)
# Gunakan di main.py dengan import decrypt_file
# -----------------------------------------

import os
import secrets
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# ---- Internal fungsi ----
def _derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    """Generate AES 256-bit key dari password dan salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())


# ---- Enkripsi ----
def encrypt_file(plain_path: str, out_path: str, password: str):
    """
    Enkripsi file ke AES-GCM.
    Format file output: [16 bytes salt][12 bytes nonce][ciphertext].
    """
    with open(plain_path, "rb") as f:
        data = f.read()

    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(12)
    key = _derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    with open(out_path, "wb") as f:
        f.write(salt + nonce + ciphertext)

    os.chmod(out_path, 0o400)
    print(f"[✅] Berhasil Load -> {out_path}")


# ---- Dekripsi ----
def decrypt_file(enc_path: str, out_path: str, password: str) -> bool:
    """
    Dekripsi file terenkripsi AES-GCM.
    Return True jika sukses, False jika password salah atau file rusak.
    """
    try:
        with open(enc_path, "rb") as f:
            blob = f.read()
        salt, nonce, ciphertext = blob[:16], blob[16:28], blob[28:]
        key = _derive_key(password, salt)
        aesgcm = AESGCM(key)
        plain = aesgcm.decrypt(nonce, ciphertext, None)

        with open(out_path, "wb") as f:
            f.write(plain)
        os.chmod(out_path, 0o400)
        return True
    except Exception:
        return False


# ---- Enkripsi string langsung ke file (opsional) ----
def encrypt_string_to_file(content: str, out_path: str, password: str):
    """Simpan string terenkripsi langsung ke file .enc"""
    tmp = out_path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(content.encode())
    encrypt_file(tmp, out_path, password)
    os.remove(tmp)