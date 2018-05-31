import pytest

from genesis_blockchain_tools.convert import *

def test_fill_from_left():
    src = "abc"
    assert len(fill_from_left(src)) == 64
    assert fill_from_left(src) == "0000000000000000000000000000000000000000000000000000000000000abc"

