from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# This global variable determines the block size in bytes for the AES
BLOCK_SIZE = 16


# This function takes in a key and plaintext string. It will encrypt this string via an AES cipher
# It then returns an encoded string in base 64 that contains the IV and ciphertext
def encrypt_data(key: bytes, plaintext: str) -> str:
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), BLOCK_SIZE)
    encrypted = cipher.encrypt(padded_data)
    return base64.b64encode(iv + encrypted).decode('utf-8')


# This function takes in a key and a string that is a base 64 cipher.
# It will then decrypt said string by getting the original cipher
# It then returns the plain text string
def decrypt_data(key: bytes, b64_ciphertext: str) -> str:
    try:
        raw = base64.b64decode(b64_ciphertext)
        iv = raw[:BLOCK_SIZE]
        encrypted = raw[BLOCK_SIZE:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted), BLOCK_SIZE)
        return decrypted.decode('utf-8')
    except Exception:
        return "[DECRYPT_ERROR]"
