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
    raise ImportError("None of fastecdsa, ecdsa, ecpy or rubenesque ECDSA modules found")
