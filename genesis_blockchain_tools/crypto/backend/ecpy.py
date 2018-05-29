from hashlib import sha256
from binascii import a2b_base64, hexlify
from os import urandom

from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA

from ..formatters import encode_sig

class CurveByAttrName:
    @property
    def P256(self):
        return Curve.get_curve('secp256r1')

curve = CurveByAttrName()

def point_to_hex_str(key):
    return format(key.W.x, 'x') + format(key.W.y, 'x')

def _gen_private_key(curve):
    """Generate a private key to sign data with.

    The private key :math:`d` is an integer generated via a cryptographically secure random number
    generator that lies in the range :math:`[1,n)`, where :math:`n` is the curve order. The specific
    random number generator used is /dev/urandom.

    Args:
        curve: The curve over which the key will be calulated.

    Returns:
        long: Returns a positive integer smaller than the curve order.
    """
    order_bits = 0
    order = curve.order

    while order > 0:
        order >>= 1
        order_bits += 1

    order_bytes = (order_bits + 7) // 8  # urandom only takes bytes
    extra_bits = order_bytes * 8 - order_bits  # bits to shave off after getting bytes

    rand = int(hexlify(urandom(order_bytes)), 16)
    rand >>= extra_bits

    # no modding by group order or we'll introduce biases
    while rand >= curve.order:
        rand = int(hexlify(urandom(order_bytes)), 16)
        rand >>= extra_bits

    return rand

def gen_private_key(curve=curve.P256):
    priv_key = _gen_private_key(curve)
    return format(priv_key, 'x')

def get_public_key(priv_key, curve=curve.P256):
    priv_key = int(priv_key, 16)
    pub_key_obj = ECPrivateKey(priv_key, curve).get_public_key()
    return point_to_hex_str(pub_key_obj)

def gen_keypair(curve=curve.P256):
    priv_key = _gen_private_key(curve)
    pub_key_obj = ECPrivateKey(priv_key, curve).get_public_key()
    return format(priv_key, 'x'), point_to_hex_str(pub_key_obj)


class ECDSAWithSize(ECDSA):
    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop('size', 64)
        super(ECDSAWithSize, self).__init__(*args, **kwargs)

    def _do_sign(self, msg, pv_key, k, canonical=False):
        if (pv_key.curve == None):
            raise ECPyException('private key haz no curve')
        curve = pv_key.curve
        n = curve.order
        G = curve.generator
        k = k%n

        msg = int.from_bytes(msg, 'big')
        
        Q = G*k
        kinv = pow(k,n-2,n)
        r = Q.x % n
        if r == 0:
            return None

        s = (kinv*(msg+pv_key.d*r)) %n
        if s == 0:
            return None

        if canonical and (s > (n//2)):
            s = n-s
        
        sig = encode_sig(r, s, fmt=self.fmt, size=self.size)
        
        return sig

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, sign_fmt='DER', 
         sign_size=32):
    priv_key_int = int(priv_key, 16)
    priv_key_obj = ECPrivateKey(priv_key_int, curve)
    signer = ECDSAWithSize(fmt=sign_fmt, size=sign_size)
    signature = signer.sign(data.encode(), priv_key_obj).hex()
    return signature

