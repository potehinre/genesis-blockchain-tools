import imp
import os

__BACKEND_NAMES = ('fastecdsa', 'ecdsa', 'ecpy', 'rubenesque')

def import_crypto_by_backend(name):
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not name in __BACKEND_NAMES:
        raise ImportError("%s crypto backend isn't available" % name)
    path = basedir
    l = []
    for i in range(0, 3):
        path, part = os.path.split(path)
        l.insert(0, part)
    return imp.load_source('.'.join(l), os.path.join(basedir, name + '.py'))

found_module = None

try:
    import fastecdsa
    found_module = 'fastecdsa'
except ImportError:
    pass

try:
    import ecdsa
    found_module = 'ecdsa'
except ImportError:
    pass

try:
    import ecpy
    found_module = 'ecpy'
except ImportError:
    pass

try:
    import rubenesque
    found_module = 'rubenesque'
except ImportError:
    pass

if found_module == 'fastecdsa':
    from .fastecdsa import (
        gen_private_key,
        get_public_key,
        gen_keypair,
        sign,
    )
elif found_module == 'ecdsa':
    from .ecdsa import (
        gen_private_key,
        get_public_key,
        gen_keypair,
        sign,
    )
elif found_module == 'ecpy':
    from .ecpy import (
        gen_private_key,
        get_public_key,
        gen_keypair,
        sign,
    )
elif found_module == 'rubenesque':
    from .rubenesque import (
        gen_private_key,
        get_public_key,
        gen_keypair,
        sign,
    )
else:
    raise ImportError("None of %s ECDSA modules found" % ', '.join(__BACKEND_NAMES))
