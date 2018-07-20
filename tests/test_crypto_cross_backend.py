import pytest
import random
import string

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

def test_get_public_key():
    assert crypto_backends
    priv_pub_keys = (

        ("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d",
         "bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601", None),

        ("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202",
         "229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d", None),

        ("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c",
         "1aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8", None),

        ("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d",
         "bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601", 'RAW'),

        ("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202",
         "229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d", 'RAW'),

        ("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c",
         "1aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8", 'RAW'),

        ("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d",
         "04bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601", '04'),

        ("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202",
         "04229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d", '04'),

        ("a4e367a69da5873ee263c48c9942438f6af1174d24555f27f71a4e910a2c9b8c",
         "041aa659b99b0bc6104aabb5dea68e3b7c627c591e3e4750bc0e450b59e35ff55a76f102594f1b86900f1d641ebbf49ce41a9cf7ef781f27da09ce2098361ef1b8", '04'),

    )

    for priv_key, e_pub_key, fmt in priv_pub_keys:
        print("priv_key: %s e_pub_key: %s fmt: %s" % (priv_key, e_pub_key, fmt))
        for crypto in crypto_backends:
            kwargs = {'fmt': fmt} if fmt else {}
            assert crypto.get_public_key(priv_key, **kwargs) == e_pub_key

def test_gen_keypair_get_public_key():
    assert crypto_backends
    tries = 3
    for i in range(1, tries):
        pub_key_fmt = get_rand_pub_key_fmt()
        gen_kw = {'pub_key_fmt': pub_key_fmt} if pub_key_fmt else {}
        get_kw = {'fmt': pub_key_fmt} if pub_key_fmt else {}
        priv_key, gen_pub_key = get_rand_backend().gen_keypair(**gen_kw)
        for crypto in crypto_backends:
            get_pub_key = get_rand_backend().get_public_key(priv_key, **get_kw)
            print("priv_key: %s gen_pub_key: %s get_pub_key: %s" % (priv_key,
                  gen_pub_key, get_pub_key))
            assert gen_pub_key == get_pub_key

def test_gen_keypair_get_public_key():
    assert crypto_backends
    tries = 8
    for i in range(1, tries):
        print("I: %s" % i)
        pub_key_fmt = get_rand_pub_key_fmt()
        gen_kw = {'pub_key_fmt': pub_key_fmt} if pub_key_fmt else {}

        sign_fmt = get_rand_sign_fmt()
        sign_kw = {'sign_fmt': sign_fmt} if sign_fmt else {}
        ver_kw = {}
        if sign_fmt:
            ver_kw['sign_fmt'] = sign_fmt
        if pub_key_fmt:
            ver_kw['pub_key_fmt'] = pub_key_fmt

        data = gen_rand_str()
        crypto = get_rand_backend()
        priv_key, pub_key = crypto.gen_keypair(**gen_kw)
        signature  = get_rand_backend().sign(priv_key, data, **sign_kw)
        print("crypto: %s priv_key: %s pub_key: %s data: %s: signature: %s gen_kw: %s sign_kw: %s ver_kw: %s" \
                % (crypto.backend_name, priv_key, pub_key, data, signature,
                    gen_kw, sign_kw, ver_kw))

        for crypto in crypto_backends:
            print("verifying by %s's verify function" % crypto.backend_name)
            assert get_rand_backend().verify(pub_key, data, signature, **ver_kw)
