import imp
import os
import sys

__BACKEND_NAMES = ('fastecdsa', 'ecdsa', 'ecpy', 'rubenesque')
__EXPORTED_NAMES = ('gen_private_key', 'get_public_key', 'gen_keypair', 'sign')

def import_crypto_by_backend(name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not name in __BACKEND_NAMES:
        raise ImportError("%s crypto backend isn't available" % name)
    path = basedir
    l = []
    for i in range(0, 3):
        path, part = os.path.split(path)
        l.insert(0, part)
    l.append(name)
    return imp.load_source('.'.join(l), os.path.join(basedir, name + '.py'))

def get_backend_names():
    return __BACKEND_NAMES

def get_available_backend_names():
    l = []
    for name in __BACKEND_NAMES:
        try:
            __import__(name)
            l.append(name)
        except ImportError as e:
            pass
    return tuple(l)

def get_first_available_backend_name():
    for name in __BACKEND_NAMES:
        try:
            __import__(name)
            return name
        except ImportError as e:
            pass

def get_first_available_backend_module():
    name = get_first_available_backend_name()
    if not name:
        raise ImportError("None of %s ECDSA modules found" % ', '.join(__BACKEND_NAMES))
    return import_crypto_by_backend(name)

def import_backend_namespace(mod, names=tuple()):
    for name in names:
        globals()[name] = getattr(mod, name)

def import_first_available_backend_namespace():
    mod =  get_first_available_backend_module()
    import_backend_namespace(mod, __EXPORTED_NAMES)

if __name__ == '__main__':
    pass
else:
    backend_name = get_first_available_backend_name()
    import_first_available_backend_namespace()
