import pytest

from genesis_blockchain_tools.crypto.backend import (
    import_crypto_by_backend, get_available_backend_names
)

from genesis_blockchain_tools.crypto.formatters import (
    encode_sig, decode_sig
)

from .utils import (
    gen_rand_str, get_rand_pub_key_fmt, get_rand_sign_fmt, get_rand_sign_fmt
)

crypto_backends = []
backends_excludes = []
for backend_name in get_available_backend_names():
    if backend_name not in backends_excludes:
        crypto_backends.append(import_crypto_by_backend(backend_name))
print("crypto_backends: %s" % ([c.backend_name for c in crypto_backends]))

def get_rand_backend():
    assert crypto_backends
    return random.choice(crypto_backends)

def _test_gen_private_key(crypto):
    priv_key = crypto.gen_private_key()
    priv_key2 = crypto.gen_private_key()
    assert priv_key != priv_key2

def test_gen_private_key():
    assert crypto_backends
    for crypto in crypto_backends:
        print("crypto.backend_name: %s" % crypto.backend_name)
        _test_gen_private_key(crypto)


def _test_get_public_key(crypto):
    assert crypto.get_public_key("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d") == "bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601"
    assert crypto.get_public_key("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202") == "229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d"
    assert crypto.get_public_key("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c") == "1aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8"

    assert crypto.get_public_key("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d", fmt='RAW') == "bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601"
    assert crypto.get_public_key("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202", fmt='RAW') == "229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d"
    assert crypto.get_public_key("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c", fmt='RAW') == "1aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8"

    assert crypto.get_public_key("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d", fmt='04') == "04bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601"
    assert crypto.get_public_key("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202", fmt='04') == "04229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d"
    assert crypto.get_public_key("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c", fmt='04') == "041aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8"

def test_get_public_key():
    assert crypto_backends
    for crypto in crypto_backends:
        print("crypto.backend_name: %s" % crypto.backend_name)
        _test_get_public_key(crypto)


def _test_gen_keypair(crypto):
    priv_key, pub_key = crypto.gen_keypair()
    assert priv_key != pub_key
    assert len(pub_key) == 2 * len(priv_key)
    pub_key2 = crypto.get_public_key(priv_key)
    assert pub_key == pub_key2

    priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='RAW')
    assert priv_key != pub_key
    assert len(pub_key) == 2 * len(priv_key)
    pub_key2 = crypto.get_public_key(priv_key)
    assert pub_key == pub_key2

    priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='04')
    assert priv_key != pub_key
    assert pub_key[0:2] == '04'
    assert len(pub_key) == 2 + 2 * len(priv_key)
    pub_key2 = crypto.get_public_key(priv_key, fmt='04')
    assert pub_key == pub_key2

def test_gen_keypair():
    assert crypto_backends
    for crypto in crypto_backends:
        print("crypto.backend_name: %s" % crypto.backend_name)
        _test_gen_keypair(crypto)


def _test_sign(crypto):
    data = "Another test data"
    tries = 5
    for i in range(1, tries):
        priv_key, pub_key = crypto.gen_keypair()

        signature = crypto.sign(priv_key, data)
        assert signature[0:2] == '30'
        assert signature[2+2:2+2+2] == '02'

        signature = crypto.sign(priv_key, data, sign_fmt='DER')
        assert signature[0:2] == '30'
        assert signature[2+2:2+2+2] == '02'

        signature = crypto.sign(priv_key, data, sign_fmt='RAW')
        assert len(signature) == 128

def test_sign():
    assert crypto_backends
    for crypto in crypto_backends:
        print("crypto.backend_name: %s" % crypto.backend_name)
        _test_sign(crypto)


def _test_verify(crypto):
    data = "More test data, ID: " + gen_rand_str()
    tries = 5
    for i in range(1, tries):
        priv_key, pub_key = crypto.gen_keypair()
        signature = crypto.sign(priv_key, data)
        assert crypto.verify(pub_key, data, signature) == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature) == False

        priv_key, pub_key = crypto.gen_keypair()
        signature = crypto.sign(priv_key, data, sign_fmt='RAW')
        assert crypto.verify(pub_key, data, signature, sign_fmt='RAW') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='RAW') == False

        priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='04')
        signature = crypto.sign(priv_key, data, sign_fmt='RAW')
        assert crypto.verify(pub_key, data, signature, sign_fmt='RAW', pub_key_fmt='04') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='RAW', pub_key_fmt='04') == False

        priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='RAW')
        signature = crypto.sign(priv_key, data, sign_fmt='RAW')
        assert crypto.verify(pub_key, data, signature, sign_fmt='RAW', pub_key_fmt='RAW') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='RAW', pub_key_fmt='RAW') == False


        priv_key, pub_key = crypto.gen_keypair()
        signature = crypto.sign(priv_key, data, sign_fmt='DER')
        assert crypto.verify(pub_key, data, signature, sign_fmt='DER') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='DER') == False

        priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='RAW')
        signature = crypto.sign(priv_key, data, sign_fmt='DER')
        assert crypto.verify(pub_key, data, signature, sign_fmt='DER', pub_key_fmt='RAW') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='DER', pub_key_fmt='RAW') == False

        priv_key, pub_key = crypto.gen_keypair(pub_key_fmt='04')
        signature = crypto.sign(priv_key, data, sign_fmt='DER')
        assert crypto.verify(pub_key, data, signature, sign_fmt='DER', pub_key_fmt='04') == True
        assert crypto.verify(pub_key, data + gen_rand_str(), signature, sign_fmt='DER', pub_key_fmt='04') == False

def test_verify():
    assert crypto_backends
    for crypto in crypto_backends:
        print("crypto.backend_name: %s" % crypto.backend_name)
        _test_verify(crypto)
