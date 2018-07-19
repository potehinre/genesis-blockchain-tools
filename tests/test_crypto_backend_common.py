from genesis_blockchain_tools.convert import fill_from_left
from genesis_blockchain_tools.crypto.backend.common import (
    point_to_hex_str, split_str_to_halves
)

def test_split_str_to_halves():
    assert split_str_to_halves('onetwo') == ('one', 'two')
    assert split_str_to_halves('01234567') == ('0123', '4567')

def test_point_to_hex_str():
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    priv_key = '15b17816c315cbc3a214edaad3661018061ef2936e63a0a93bdb7644c131ad2d'
    pub_key = 'bdbb17d50e7c0ecc23aebc0cb8e6b744e7ee3a63644f49548f6af2afcc699cd9b1ff50abed237fef39ed11efebf0a74e550c03db5caad51345ba2aeae89d3601'
    x, y = split_str_to_halves(pub_key)
    x, y = int(x, 16), int(y, 16)
    point = Point(x, y)
    x = fill_from_left(format(point.x, 'x'))
    y = fill_from_left(format(point.y, 'x'))
    p = point_to_hex_str(point)
    assert len(p) == 128
    assert p == x + y
    p = point_to_hex_str(point, fmt='04')
    assert len(p) == 130
    assert p == '04' + x + y

