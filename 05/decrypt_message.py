from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes_ecb_decrypt(ciphertext, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(cipher.algorithm.block_size).unpadder()
    padded = decryptor.update(b64d(ciphertext)) + decryptor.finalize()
    return unpadder.update(padded) + unpadder.finalize()
#read
key = ""
with open("hash_key.key", 'rb') as file:
	key = file.read()
	print("klucz", key)

enc_message = ""
with open("enc_message.txt", 'r') as file:
	enc_message = file.read().encode()
	print("zakodowana wiadomość:",enc_message)


backend = default_backend()


with open("dec_message.txt", 'wb') as file:
	print("Odkodowana wiadomość:",aes_ecb_decrypt(enc_message,key))
	file.write(aes_ecb_decrypt(enc_message,key))