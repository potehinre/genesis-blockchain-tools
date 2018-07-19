try:
    import cryptography
    run_main_part = True
except ImportError as e:
    run_main_part = False

if run_main_part:
    from genesis_blockchain_tools.convert import fill_from_left
    from genesis_blockchain_tools.crypto.backend.cryptography import (
        point_to_hex_str, ec, curve, backend
    )

    def test_point_to_hex_str():
        point = ec.generate_private_key(curve.P256, backend).public_key().public_numbers()
        x = fill_from_left(format(point.x, 'x'))
        y = fill_from_left(format(point.y, 'x'))
        p = point_to_hex_str(point)
        assert len(p) == 128
        assert p == x + y
        p = point_to_hex_str(point, fmt='04')
        assert len(p) == 130
        assert p == '04' + x + y
else:
    print("cryptography backend skipped")
