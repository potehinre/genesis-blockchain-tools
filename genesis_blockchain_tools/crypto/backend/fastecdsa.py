from fastecdsa import keys, curve, ecdsa
from fastecdsa.point import Point
from hashlib import sha256

from ..formatters import encode_sig
from ...convert import int_to_hex_str

backend_name = 'fastecdsa'

def point_to_hex_str(key, fmt='RAW'):
    hex_str = int_to_hex_str(key.x) + int_to_hex_str(key.y)
    if fmt == 'RAW':
        return hex_str
    elif fmt == '04':
        return '04' + hex_str

#def gen_private_key(curve=curve.P256):
def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key = keys.gen_private_key(curve)
    return format(priv_key, 'x')

#def get_public_key(priv_key, curve=curve.P256):
def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256, fmt='RAW'):
    priv_key = int(priv_key, 16)
    pub_key = keys.get_public_key(priv_key, curve=curve)
    return point_to_hex_str(pub_key)

def gen_keypair(curve=curve.P256):
    if fmt in ['RAW', '04']:
        priv_key = keys.gen_private_key(curve=curve)
        pub_key = keys.get_public_key(priv_key, curve=curve)
        return format(priv_key, 'x'), point_to_hex_str(pub_key, fmt=fmt)

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER',
         sign_size=32):
    if sign_fmt == 'DER':
    r, s = ecdsa.sign(data, int(priv_key, 16), hashfunc=hashfunc)
    signature = encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    return signature
