from fastecdsa import keys, curve, ecdsa
from fastecdsa.point import Point
from hashlib import sha256

from ..formatters import encode_sig

def point_to_hex_str(key):
    return format(key.x, 'x') + format(key.y, 'x')

def gen_private_key(curve=curve.P256):
    priv_key = keys.gen_private_key(curve)
    return format(priv_key, 'x')

def get_public_key(priv_key, curve=curve.P256):
    priv_key = int(priv_key, 16)
    pub_key = keys.get_public_key(priv_key, curve=curve)
    return point_to_hex_str(pub_key)

def gen_keypair(curve=curve.P256):
    priv_key = keys.gen_private_key(curve=curve)
    pub_key = keys.get_public_key(priv_key, curve=curve)
    return format(priv_key, 'x'), point_to_hex_str(pub_key)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER',
         sign_size=64):
    r, s = ecdsa.sign(data, int(priv_key, 16), hashfunc=hashfunc)
    signature = encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    return signature
