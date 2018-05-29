from .backend import (
    gen_private_key,
    get_public_key,
    gen_keypair,
    sign,
)

def parse_signature(signature):
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
    return r, s

def parse_simple_signature(signature):
    total_len = len(signature)
    return signature[:total_len // 2], signature[total_len // 2:]

