found_module = None

try:
    import fastecdsa
    found_module = 'fastecdsa'
except ModuleNotFoundError as e:
    pass

try:
    import ecpy
    found_module = 'ecpy'
except ModuleNotFoundError as e:
    pass

try:
    import rubenesque
    found_module = 'rubenesque'
except ModuleNotFoundError as e:
    pass

if found_module == 'fastecdsa':
    from .fastecdsa import (
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
    raise ModuleNotFoundError("None of fastecdsa, ecpy or rubenesque ECSDA modules found")

class Error(Exception):
    pass

