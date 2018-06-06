try:
    from genesis_blockchain_tools.crypto.backend.fastecdsa import (
            Point, curve, point_to_hex_str
    )
    def test_point_to_hex_str():
        x = 0x60b34e6babe8fab2302ff27dd50e4e3e3f215f6e6c3b62c3b07272d2bb5046b
        y = 0x629686c5c6fecfda1fea9944e259f7e7d95569a7a33c80034121edaece4ecf1
        p = Point(x, y, curve.P256)
        assert hex(x).split('x')[1] + hex(y).split('x')[1] == point_to_hex_str(p) 
except ImportError as e:
    print("fastecdsa backend skipped")

