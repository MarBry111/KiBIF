import tinyec.ec as ec
import tinyec.registry as reg
import secrets
import base64
from Crypto.Cipher import AES
import hashlib, secrets, binascii


# y^2 = x^3 + ax^2 +b 
a = 2
b = 3

#start point
point = (22,5)

field = ec.SubGroup(97, point, 2000, 1)
#curve = reg.get_curve('brainpoolP256r1')
curve =  ec.Curve(a, b, field)

def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]

def ecc_calc_encryption_keys(pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    sharedECCKey = pubKey * ciphertextPrivKey
    return (sharedECCKey, ciphertextPubKey)

def ecc_calc_decryption_key(privKey, ciphertextPubKey):
    sharedECCKey = ciphertextPubKey * privKey
    return sharedECCKey

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 64, 'big'))
    sha.update(int.to_bytes(point.y, 64, 'big'))
    return sha.digest()

privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g

print("private key:", hex(privKey))
print("public key:", compress_point(pubKey))

(encryptKey, ciphertextPubKey) = ecc_calc_encryption_keys(pubKey)
print("ciphertext pubKey:", compress_point(ciphertextPubKey))
print("encryption key:", compress_point(encryptKey))

decryptKey = ecc_calc_decryption_key(privKey, ciphertextPubKey)
print("decryption key:", compress_point(decryptKey))

with open('key.key', 'w') as file:
	key = compress_point(decryptKey)
	print(key)
	file.write(key)

with open('hash_key.key', 'wb') as file:
	key = ecc_point_to_256_bit_key(decryptKey)
	print(key)
	file.write(key)

