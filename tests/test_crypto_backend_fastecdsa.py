try:
    import fastecdsa
    run_main_part = True
except ImportError as e:
    run_main_part = False

if run_main_part:
    from genesis_blockchain_tools.convert import fill_from_left
    from genesis_blockchain_tools.crypto.backend.fastecdsa import (
        Point, curve, keys, point_to_hex_str
    )

    def test_point_to_hex_str():
        priv_key = keys.gen_private_key(curve=curve.P256)
        point = keys.get_public_key(priv_key, curve=curve.P256)
        x = fill_from_left(format(point.x, 'x'))
        y = fill_from_left(format(point.y, 'x'))
        p = point_to_hex_str(point)
        assert len(p) == 128
        assert p == x + y
        p = point_to_hex_str(point, fmt='04')
        assert len(p) == 130
        assert p == '04' + x + y
else:
    print("fastecdsa backend skipped")
