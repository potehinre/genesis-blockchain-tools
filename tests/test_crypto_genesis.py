import pytest

from genesis_blockchain_tools.crypto import (
    gen_private_key,
    get_public_key,
    gen_keypair,
)
from genesis_blockchain_tools.crypto.genesis import (
    checksum, public_key_to_address, double_hash
)
def test_checksum():
    assert checksum("some string".encode()) == 9
    assert checksum("another string".encode()) == 2
    assert checksum("jeez, it's so boring".encode()) == 0
    assert checksum("and final one".encode()) == 7
    assert checksum("#34423".encode()) == 1

def test_public_key_to_address():
    priv_key = gen_private_key()
    assert public_key_to_address("some string".encode()) == 6973694608268913209
    assert public_key_to_address("another string".encode()) == 826786831444702840
    assert public_key_to_address("jeez, it's so boring".encode()) == -1106672694297211255
    assert public_key_to_address("and final one".encode()) == -5961772402273559210
    assert public_key_to_address("#34423".encode()) == 6729523148133476469 

def test_double_hash():
    assert double_hash("some string".encode()) == bytearray([190, 71, 146, 194, 68, 74, 231, 230, 180, 206, 236, 27, 236, 231, 72, 142, 255, 142, 193, 16, 191, 23, 17, 134, 130, 233, 238, 189, 116, 61, 77, 16])

