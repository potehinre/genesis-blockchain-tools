import pytest

from genesis_blockchain_tools.convert import *

def test_fill_from_left():
    src = "abc"
    assert len(fill_from_left(src)) == 64
    assert fill_from_left(src) == "0000000000000000000000000000000000000000000000000000000000000abc"

def test_int_to_hex_str():
    assert int_to_hex_str(123456789) == '00000000000000000000000000000000000000000000000000000000075bcd15'
    assert int_to_hex_str(1234) == '00000000000000000000000000000000000000000000000000000000000004d2'

