from genesis_blockchain_tools.convert import fill_from_left

try:
    from genesis_blockchain_tools.crypto.backend.cryptography import (
            int_to_hex_str, point_to_hex_str, ec, curve, backend
    )

    def test_int_to_hex_str():
        assert int_to_hex_str(123456789) == '00000000000000000000000000000000000000000000000000000000075bcd15'
        assert int_to_hex_str(1234) == '00000000000000000000000000000000000000000000000000000000000004d2'

    def test_point_to_hex_str():
        point = ec.generate_private_key(curve.P256, backend).public_key().public_numbers()
        x = fill_from_left(format(point.x, 'x'))
        y = fill_from_left(format(point.y, 'x'))
        p = point_to_hex_str(point)
        assert len(p) == 128
        assert p == x + y

except ImportError as e:
    print("cryptography backend skipped")
