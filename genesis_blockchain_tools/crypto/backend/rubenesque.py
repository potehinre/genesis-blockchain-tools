from rubenesque.codecs.sec import encode, decode
from rubenesque.signatures import ecdsa
import rubenesque.curves
from hashlib import sha256


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


def sign(priv_key, data, hashfunc=sha256, curve=curve.P256, options={}):
    h = hashfunc(data.encode('utf-8')).digest()
    while True:
        r, s = ecdsa.sign(curve, int(priv_key, 16), h)
        r, s = format(r, 'x'), format(s, 'x')
        r_len = format(len(r) // 2, 'x')
        s_len = format(len(s) // 2, 'x')
        total_len = format((len(r) // 2) + (len(s) // 2) + 4, 'x')
        signature = '30' + total_len + '02' + r_len + r + '02' + s_len + s
        if not options.get('no_odd_total_len', False) \
        or int(signature[2:4], 16) %2 == 0:
            return signature 

