# AES：mode:'CBC';  padding: 'AnsiX923';  iv: 8;

from Crypto import Random
from Crypto.Cipher import AES


def pad(data):
    length = 16 - (len(data) % 16)
    return data + (chr(length)*length).encode()


def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]


def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    from hashlib import sha512
    assert len(salt) == 8, len(salt)
    data += salt
    key = sha512(data).digest()
    final_key = key
    while len(final_key) < output:
        key = sha512(key + data).digest()
        final_key += key
    return final_key[:output]


def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return salt + aes.encrypt(pad(message))


def decrypt(encrypted, passphrase):
    salt = encrypted[0:8]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[8:]))


if __name__ == '__main__':
    from uuid import uuid4
    plaintext = uuid4().hex.encode()
    key = uuid4().hex.encode()
    cipher = encrypt(plaintext, key)
    plaintext_ = decrypt(cipher, key)
    print(plaintext)
    print(cipher)
    print(plaintext_)
    assert plaintext == plaintext_
