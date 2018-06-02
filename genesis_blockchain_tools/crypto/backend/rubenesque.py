from rubenesque.codecs.sec import encode, decode
from rubenesque.signatures import ecdsa
import rubenesque.curves
from hashlib import sha256

from ..formatters import encode_sig

backend_name = 'rubenesque'

class CurveByAttrName:
    @property
    def P256(self):
        return rubenesque.curves.find('secp256r1')

curve = CurveByAttrName()

def point_to_hex_str(key):
    return format(key.x, 'x') + format(key.y, 'x')

def gen_private_key(curve=curve.P256):
    priv_key = curve.private_key()
    return format(priv_key, 'x')

def get_public_key(priv_key, curve=curve.P256):
    priv_key = int(priv_key, 16)
    pub_key_obj = curve.generator() * priv_key
    return point_to_hex_str(pub_key_obj)

def gen_keypair(curve=curve.P256):
    priv_key = gen_private_key(curve=curve)
    pub_key = get_public_key(priv_key)
    return priv_key, pub_key

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER',
         sign_size=64):
    h = hashfunc(data.encode('utf-8')).digest()
    r, s = ecdsa.sign(curve, int(priv_key, 16), h)
    signature = encode_sig(r, s, fmt=sign_fmt, size=sign_size).hex()
    return signature

