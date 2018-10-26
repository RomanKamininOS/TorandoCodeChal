import hashlib
import rsa

from tornado.options import options


def sha_hash(password):
    return hashlib.sha512(password.encode('utf-8') + options.SALT.encode('utf-8')).hexdigest()


def generate_keys(n=1024):
    (pubkey, privkey) = rsa.newkeys(n)
    with open('../private.pem', 'wb') as f:
        f.write(privkey.save_pkcs1('PEM'))

    with open('../public.pem', 'wb') as f:
        f.write(pubkey.save_pkcs1('PEM'))


if __name__ == '__main__':
    generate_keys()
    with open('../private.pem', 'rb') as f:
        private = rsa.PrivateKey.load_pkcs1(f.read())

    with open('../public.pem', 'rb') as f:
        public = rsa.PublicKey.load_pkcs1(f.read())

    crypto = rsa.encrypt('test message for encryption'.encode('utf8'), public)
    decrypt = rsa.decrypt(crypto, private)
    print(decrypt)
