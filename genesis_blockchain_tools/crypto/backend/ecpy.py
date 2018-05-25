from hashlib import sha256
from binascii import a2b_base64, hexlify
from os import urandom

from ecpy.curves import Curve, Point
from ecpy.keys import ECPublicKey, ECPrivateKey
from ecpy.ecdsa import ECDSA

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

def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, options={}):
    priv_key_int = int(priv_key, 16)
    priv_key_obj = ECPrivateKey(priv_key_int, curve)
    signer = ECDSA()
    while True:
        signature = signer.sign(data.encode(), priv_key_obj).hex()
        if not options.get('no_odd_total_len', False) \
        or int(signature[2:4], 16) %2 == 0:
            return signature 

