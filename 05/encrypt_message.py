from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

#read
key = ""
with open("hash_key.key", 'rb') as file:
	key = file.read()
	print("klucz:",key)

message = ""
with open("message.txt", 'r') as file:
	message = file.read().encode()
	print("wiadomość:",message)


backend = default_backend()

def aes_ecb_encrypt(message, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(cipher.algorithm.block_size).padder()
    padded = padder.update(message) + padder.finalize()
    return b64e(encryptor.update(padded) + encryptor.finalize())



encrypted = aes_ecb_encrypt(message,key)

with open('enc_message.txt', 'wb') as file:
	print("zakodowana wiadomość:",encrypted)
	file.write(encrypted)