from ecdsa import SigningKey, NIST256p
from ecdsa.util import sigencode_der

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

#from hashlib import sha256

backend_name = 'cryptography'
backend = default_backend()

class CurveByAttrName:
    @property
    def P256(self):
        return ec.SECP256R1()

curve = CurveByAttrName()
sha256 = hashes.SHA256()

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = ec.generate_private_key(ec.SECP256R1(), backend)
    return format(priv_key.private_numbers().private_value, 'x')

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256):
    priv_key = int(priv_key, 16)
    priv_key = ec.derive_private_key(priv_key, ec.SECP256R1(), backend)
    x = priv_key.public_key().public_numbers().x
    y = priv_key.public_key().public_numbers().y
    return format(x, 'x') + format(y, 'x')

def gen_keypair(curve=curve.P256, hashfunc=sha256):
    priv_key = ec.generate_private_key(ec.SECP256R1(), backend)
    x = priv_key.public_key().public_numbers().x
    y = priv_key.public_key().public_numbers().y
    return format(priv_key.private_numbers().private_value, 'x'), \
           format(x, 'x') + format(y, 'x')

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    data = data.encode()
    priv_key = int(priv_key, 16)
    priv_key = ec.derive_private_key(priv_key, ec.SECP256R1(), backend)
    if sign_fmt == "DER":
        signature = priv_key.sign(data, ec.ECDSA(hashfunc)).hex()
    else:
        signature = None
    return signature
