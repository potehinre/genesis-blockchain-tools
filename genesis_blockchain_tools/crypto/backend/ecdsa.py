from ecdsa import SigningKey, NIST256p
from ecdsa.util import sigencode_der

from hashlib import sha256

class CurveByAttrName:
    @property
    def P256(self):
        return NIST256p

curve = CurveByAttrName()

def gen_private_key(curve=curve.P256, hashfunc=sha256):
    priv_key =  SigningKey.generate(curve=curve, hashfunc=hashfunc)
    return priv_key.to_string().hex()

def get_public_key(priv_key, curve=curve.P256, hashfunc=sha256):
    priv_key = bytes.fromhex(priv_key)
    priv_key = SigningKey.from_string(priv_key, curve=curve, hashfunc=hashfunc)
    return priv_key.get_verifying_key().to_string().hex()

def gen_keypair(curve=curve.P256, hashfunc=sha256):
    priv_key =  SigningKey.generate(curve=curve, hashfunc=hashfunc)
    pub_key = priv_key.get_verifying_key()
    return priv_key.to_string().hex(), pub_key.to_string().hex()

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    data = data.encode()
    priv_key = bytes.fromhex(priv_key)
    priv_key = SigningKey.from_string(priv_key, curve=curve, hashfunc=hashfunc)
    if sign_fmt == "DER":
        signature = priv_key.sign(data, hashfunc=hashfunc, sigencode=sigencode_der)
    else:
        signature = priv_key.sign(data, hashfunc=hashfunc)
    return signature.hex()
