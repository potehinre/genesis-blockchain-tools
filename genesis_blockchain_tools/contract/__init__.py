import datetime 
import os
import msgpack
import random
import subprocess
import binascii
from random import randint

from ..crypto import sign, get_public_key
from ..convert import encode_length_plus_data
from ..crypto.genesis import public_key_to_address, double_hash

from .fields import (
    Field, IntegerField, StringField, BooleanField, MoneyField, FloatField,
    ArrayField, BytesField, FileField,
)

class Error(Exception): pass
class SchemaIsNotSetError(Error): pass
class PublicKeyIsNotSetError(Error): pass
class NonOptionalParamIsNotSetError(Error): pass
class UnknownParamTypeError(Error): pass
class UnknownParamError(Error): pass

def binsign(pk, data):
    with open('tx', 'wb') as f:
        f.write(data)
    output = subprocess.check_output(['./signtool', pk, 'tx']).rstrip()
    return output

class Contract:
    def serialize(self):
        return msgpack.packb(self.get_struct(), use_bin_type=True)

    def calc_hash(self):
        bin_signatures = self.bin_signatures
        self.bin_signatures = None
        hsh = double_hash(self.serialize())
        self.bin_signatures = bin_signatures
        return hsh

    def sign(self):
        return binascii.unhexlify(binsign(self.private_key, self.serialize()))

    def concat(self):
        return self.serialize()

    def get_struct(self):
        files = {}
        for name, path in self.files.items():
            with open(path, "rb") as f:
                    data = f.read()
                    hsh = double_hash(data)
                    mime = "Content-Type: application/json"
                    files[name] = {"FileHeader": {"Hash": hsh, "MimeType": mime}, "Data": data}
        d = {
            'Header': {
                'Time': self.time,
                'Name': self.name,
                'Nonce': self.nonce,
                'EcosystemID': self.ecosystem_id,
                'KeyID': self.key_id,
                'NetworkID': self.network_id,
                'PublicKey': self.public_key,
                'BinSignatures': self.bin_signatures,
            },
            'Params': self.params,
            'Files': files,
        }
        return d

    def __init__(self, *args, **kwargs):
        self.tx_header = kwargs.get('tx_header', bytes([0x80]))
        self.id = kwargs.get('id', kwargs.get('ID', None))
        self.time = kwargs.get('time',
                               kwargs.get('Time', 
                               int(datetime.datetime.now().timestamp())))
        random.seed()
        self.nonce = kwargs.get('nonce', kwargs.get('Nonce',
                                                 randint(0, 10000000000000)))
        self.ecosystem_id = kwargs.get('ecosystem_id',
                                       kwargs.get('EcosystemID', 1))
        self.network_id = kwargs.get('network_id',
                                      kwargs.get('NetworkID', 1))
        self.token_ecosystem = kwargs.get('token_ecosystem',
                                          kwargs.get('TokenEcosystem', 0))
        self.signed_by = kwargs.get('signed_by', 
                                    kwargs.get('SignedBy', '0'))
        self.bin_signatures = kwargs.get('bin_signatures',
                                         kwargs.get('BinSignatures', None))
        self.private_key = kwargs.get('private_key', None)
        self.public_key = kwargs.get('public_key',
                    kwargs.get('PublicKey',
                               bytes.fromhex(get_public_key(self.private_key))))
        if not self.public_key:
            PublicKeyIsNotSetError(self.public_key)
        self.key_id = public_key_to_address(self.public_key)
        self.max_sum = kwargs.get('max_sum', kwargs.get('MaxSum', ''))
        self.pay_over = kwargs.get('pay_over', kwargs.get('PayOver', ''))
        self.params = kwargs.get('params', kwargs.get('Params', {}))
        self.files = kwargs.get('files', kwargs.get('Files', {}))
        self.name = kwargs.get('name', kwargs.get('Name', {}))
        self.bin_signatures = self.sign()
