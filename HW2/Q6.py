from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import binascii

def to_hex(b: bytes) -> str:
    return binascii.hexlify(b).decode()

def pad(data: bytes) -> bytes:
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_ecb(key: bytes, plaintext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext))

def decrypt_ecb(key: bytes, ciphertext: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext))

def encrypt_cbc(key: bytes, plaintext: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext))

def decrypt_cbc(key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))

key = bytes.fromhex('02020202020202020202020202020202')
plaintext_str = "spread your wings and fly away, fly away, far away."
plaintext_bytes = plaintext_str.encode()

ciphertext_ecb = encrypt_ecb(key, plaintext_bytes)
decrypted_ecb = decrypt_ecb(key, ciphertext_ecb)

iv = get_random_bytes(16)
ciphertext_cbc = encrypt_cbc(key, plaintext_bytes, iv)
decrypted_cbc = decrypt_cbc(key, ciphertext_cbc, iv)

print("Simulating AES algorithm...")
print("plaintext:", plaintext_str)
print("IV:", to_hex(iv))

print("ciphertext (ECB):", to_hex(ciphertext_ecb))
print("ciphertext (CBC):", to_hex(ciphertext_cbc))

print("decrypted (ECB):", decrypted_ecb.decode())
print("decrypted (CBC):", decrypted_cbc.decode())

if plaintext_bytes == decrypted_ecb == decrypted_cbc:
    print("\nresult of an encryption followed by a decryption using the same key is equal to the original message.")
else:
    print("\nfailed.")