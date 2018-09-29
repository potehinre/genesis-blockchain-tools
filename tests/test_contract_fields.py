import os
import pytest
import tempfile

from genesis_blockchain_tools.contract.fields import (
    Field, IntegerField, StringField, BooleanField, MoneyField, FloatField,
    ArrayField, BytesField, FileField,
)

def test_field_object():
    f = Field()
    f.value = 3
    assert f.value == 3

    f = Field(4)
    assert f.value == 4

def test_integer_field():
    i = IntegerField()
    i.value = 3
    assert i.value == 3

    i = IntegerField(4)
    assert i.value == 4

def test_string_field():
    s = StringField()
    s.value = 3
    assert s.value == '3'

    s = StringField(4)
    assert s.value == '4'

def test_boolean_field():
    b = BooleanField()
    b.value = 3
    assert b.value == False

    b = BooleanField(4)
    assert b.value == False

def test_money_field():
    m = MoneyField()
    m.value = 3
    assert m.value == '3'

    m = MoneyField(4)
    assert m.value == '4'

def test_float_field():
    f = FloatField()
    f.value = 3
    assert f.value == float(3)

    f = FloatField(4)
    assert f.value == float(4)

def test_array_field():
    a = ArrayField()
    a.value = 3
    assert a.value == tuple(['3'])

    a = ArrayField([8, 4, 1])
    assert a.value == tuple(['8', '4', '1'])

def test_bytes_field():
    b = BytesField()
    b.value = [3]
    assert b.value == bytearray([3])

def test_file_field():
    b = FileField()
    tmp_file = tempfile.mktemp()
    tmp_path = str(tmp_file)
    with open(tmp_path, 'w') as f:
        f.write("this is a test")
        f.close()
    b.path = tmp_path
    d = b.to_dict()
    assert d['Body'] == b'this is a test'
    assert d['Name'] == os.path.basename(tmp_path)


    b = FileField(name='test.txt', path=tmp_path)
    d = b.to_dict()
    assert d['Name'] == 'test.txt'
    assert d['Body'] == b'this is a test'

    d = b.value
    assert d['Name'] == 'test.txt'
    assert d['Body'] == b'this is a test'

