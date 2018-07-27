from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


class RSAKey:
    def save(self, filename: str):
        with open(filename, 'wb') as f:
            f.write(self.serialize())

    def load(self, filename: str):
        with open(filename, 'rb') as f:
            self.deserialize(f.read())
        return self

    @staticmethod
    def serialize():
        assert None, 'abstract method'
        return b''

    @staticmethod
    def deserialize(content: bytes):
        assert content
        assert None, 'abstract method'


class RSAPrivateKey(RSAKey):
    def __init__(self, private_key=None):
        self.private_key = private_key

    def sign(self, message: bytes):
        return self.private_key.sign(message, padding.PKCS1v15(), hashes.SHA512())

    def decrypt(self, cipher: bytes):
        return self.private_key.decrypt(cipher, padding.PKCS1v15())

    def serialize(self):
        pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem

    def deserialize(self, pem):
        self.private_key = load_pem_private_key(pem, None, default_backend())
        return self

    def export(self):
        return RSAPublicKey(self.private_key.public_key())


class RSAPublicKey(RSAKey):
    def __init__(self, public_key=None):
        self.public_key = public_key

    def verify(self, message: bytes, signature: bytes):
        try:
            self.public_key.verify(signature, message, padding.PKCS1v15(), hashes.SHA512())
            return True
        except InvalidSignature:
            return False

    def encrypt(self, plaintext: bytes):
        return self.public_key.encrypt(plaintext, padding.PKCS1v15())

    def serialize(self):
        pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        )
        return pem

    def deserialize(self, pem):
        self.public_key = load_pem_public_key(pem, default_backend())
        return self


def gen_rsa_pair():
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    return RSAPrivateKey(key), RSAPublicKey(key.public_key())


def main():
    # private_key, public_key = gen_rsa_pair()
    with open('config/key.pem', 'rb') as f:
        private_pem = f.read()
    private_key = RSAPrivateKey().deserialize(private_pem)
    public_key = private_key.export()
    m = b'12345'
    # 加密，签名
    c = public_key.encrypt(m)
    s = private_key.sign(m)
    # 序列化
    private_pem = private_key.serialize()
    public_pem = public_key.serialize()
    # 反序列化
    private_key = RSAPrivateKey().deserialize(private_pem)
    public_key = RSAPublicKey().deserialize(public_pem)
    # 解密，验证
    assert m == private_key.decrypt(c)
    assert public_key.verify(m, s)

    # print(dir(private_key))
    # print(dir(public_key))


if __name__ == '__main__':
    main()
