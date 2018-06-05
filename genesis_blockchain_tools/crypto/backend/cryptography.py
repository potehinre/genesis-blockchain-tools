import logging

from ecdsa import SigningKey, NIST256p
from ecdsa.util import sigencode_der

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

from ...convert import fill_from_left

logger = logging.getLogger(__name__)
backend_name = 'cryptography'
backend = default_backend()

class CurveByAttrName:
    @property
    def P256(self):
        return ec.SECP256R1()

curve = CurveByAttrName()
sha256 = hashes.SHA256()

def int_to_hex_str(value, exp_len=64):
    return fill_from_left(format(value, 'x'), exp_len=exp_len, filler='0')

def point_to_hex_str(key):
    return int_to_hex_str(key.x) + int_to_hex_str(key.y)

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = ec.generate_private_key(curve, backend)
    return int_to_hex_str(priv_key.private_numbers().private_value)
    return "ac3877a3b66584ecce9ab3ab661d85aa04006cb54ca6401a3845d0cfefc97d16"

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256):
    priv_key = int(priv_key, 16)
    priv_key = ec.derive_private_key(priv_key, curve, backend)
    return point_to_hex_str(priv_key.public_key().public_numbers())

def gen_keypair(curve=curve.P256, hashfunc=sha256):
    priv_key = ec.generate_private_key(curve, backend)
    return int_to_hex_str(priv_key.private_numbers().private_value), \
           point_to_hex_str(priv_key.public_key().public_numbers())

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    data = data.encode()
    priv_key = int(priv_key, 16)
    priv_key = ec.derive_private_key(priv_key, curve, backend)
    if sign_fmt == "DER":
        return priv_key.sign(data, ec.ECDSA(hashfunc)).hex()
