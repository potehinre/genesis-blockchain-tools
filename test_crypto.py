import pytest

from genesis_blockchain_tools.crypto import *


try:
    from genesis_blockchain_tools.crypto.backend.fastecdsa import (
            Point, curve, point_to_hex_str
    )
    def test_point_to_hex_str():
        x = 0x60b34e6babe8fab2302ff27dd50e4e3e3f215f6e6c3b62c3b07272d2bb5046b
        y = 0x629686c5c6fecfda1fea9944e259f7e7d95569a7a33c80034121edaece4ecf1
        p = Point(x, y, curve.P256)
        assert hex(x).split('x')[1] + hex(y).split('x')[1] == point_to_hex_str(p) 
except ModuleNotFoundError as e:
    pass

def test_gen_private_key():
    priv_key = gen_private_key()
    priv_key2 = gen_private_key()
    assert priv_key != priv_key2


def test_get_public_key():
    assert get_public_key("15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d") == "bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601"
    assert get_public_key("2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202") == "229ec0d7b943f5e2c2558237c93d9e1e7d5b5cda84d34cfdb0348ec353f4809f2edb841b4ef8718bcdee012eff817fb2b254c991281ef3d563a17bc1a30e4b7d"


def test_gen_keypair():
    priv_key, pub_key = gen_keypair()
    assert priv_key != pub_key


def test_sign():
    data = "Some test data"
    priv_key, pub_key = gen_keypair()
    signature = sign(priv_key, data) 
    header = signature[:2]
    assert header == '30'
    total_len = int('0x' + signature[2:2+2], 16)
    marker1 = signature[2+2:2+2+2]
    assert marker1 == '02'
    r_len = int('0x' + signature[2+2+2:2+2+2+2], 16) * 2
    r = signature[2+2+2+2:2+2+2+2+r_len]
    marker2 = signature[2+2+2+2+r_len:2+2+2+2+r_len+2]
    assert marker2 == '02'
    s_len = int('0x' + signature[2+2+2+2+r_len+2:2+2+2+2+r_len+2+2], 16) * 2
    s = signature[2+2+2+2+r_len+2+2:2+2+2+2+r_len+2+2+s_len]
    assert len(r) // 2  + len(s) // 2 + 4 == total_len

def test_sign_no_off_total_len():
    data = "Some test data"
    priv_key, pub_key = gen_keypair()
    found_odd = False
    tries_num = 200
    for i in range(1, tries_num):
        signature = sign(priv_key, data, options={'no_odd_total_len': False}) 
        if int(signature[2:4], 16) % 2 != 0:
            print("FOUND ODD")
            found_odd = True
            break
    assert found_odd == True
    for i in range(1, tries_num):
        signature = sign(priv_key, data, options={'no_odd_total_len': True}) 
        assert int(signature[2:4], 16) % 2 == 0
