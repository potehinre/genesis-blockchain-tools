import os
import datetime
import re

class Field:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __init__(self, *args):
        if len(args) > 0:
            self.value = args[0]

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self)

class IntegerField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = int(value)

class StringField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value)

    def __repr__(self):
        return "'%s'" % str(self.value)


class MoneyField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value).replace(',', '.')

    def __repr__(self):
        return '"%s"' % str(self.value)

class BooleanField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = bool(re.search('^\s*(true|yes|1(.(0)+)?)\s*$', str(value),
                                     re.IGNORECASE))

class FloatField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = float(value)

class ArrayField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = tuple(map(lambda v: str(v), value))
        except TypeError:
            self._value = tuple([str(value)])

class BytesField(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = bytearray(tuple(map(lambda v: int(v), value)))
        except TypeError:
            print("value: %s" % value)
            self._value = bytearray([int(value)])

class FileField(Field):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, *args):
        if len(args) > 0:
            self._path = str(args[0])
        else:
            self._path = str(self._value)
        self.name = os.path.basename(self._path)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, *args):
        if len(args) > 0:
            self._name = str(args[0])
        else:
            self._name = str(self._value)

    @property
    def mime_type(self):
        return self._mime_type

    @mime_type.setter
    def mime_type(self, *args):
        if len(args) > 0:
            self._mime_type = str(args[0])
        else:
            self._mime_type = 'text/plain'

    def __init__(self, *args, **kwargs):
        if len(args) > 0:
            self.value = args[0]
        self.path = kwargs.get('path')
        if kwargs.get('name'):
            self.name = kwargs.get('name')
        if kwargs.get('body'):
            self.body = kwargs.get('body')
        self.mime_type = kwargs.get('mime_type', 'text/plain')
        self._did_read = False
        self.file_open_mode = kwargs.get('file_open_mode', 'rb')

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, *args):
        if len(args) > 0:
            self._body = args[0]

    def read(self):
        with open(self.path, self.file_open_mode) as f:
            self.body = f.read()
            f.close()
            self._did_read = True
        return self.body

    def to_dict(self):
        if not self._did_read:
            self.read()
        d = {
            'Name': self.name,
            'MimeType': self.mime_type,
            'Body': self.body,
        }
        return d

    @property
    def value(self):
        return self.to_dict()

    @value.setter
    def value(self, value):
        pass
