from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# NOTE: Make sure 'pycryptodome' is installed.
# Uninstall any package named 'crypto' (which is unrelated and will conflict).

BLOCK_SIZE = 16  # AES block size (bytes)


def encrypt_data(key: bytes, plaintext: str) -> str:
    """
    Encrypt a plaintext string using AES-CBC.
    Returns a base64-encoded string containing IV + ciphertext.
    """
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), BLOCK_SIZE)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode('utf-8')


def decrypt_data(key: bytes, b64_ciphertext: str) -> str:
    """
    Decrypt a base64-encoded ciphertext string (IV + ciphertext).
    Returns the original plaintext string.
    """
    try:
        raw = base64.b64decode(b64_ciphertext)
        iv = raw[:BLOCK_SIZE]
        encrypted = raw[BLOCK_SIZE:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), BLOCK_SIZE)
        return decrypted.decode('utf-8')
    except Exception:
        return "[DECRYPT_ERROR]"
