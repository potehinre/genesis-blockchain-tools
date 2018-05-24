Genesis BlockChain Tools
========================

Setup
-----

Manual installation:

* Activate your virtualenv
* git clone https://github.com/blitzstern5/genesis-blockchain-tools
* cd genesis-blockchain-tools
* python setup.py install

Using pip:

* Activate your virtualenv
* pip install git+https://github.com/blitzstern5/genesis-blockchain-tools

Using pip/requirements:

* Activate your virtualenv
* Add 'git+https://github.com/blitzstern5/genesis-blockchain-tools' to your requirements.txt
* pip install -r requirements.txt

Usage
-----

To get public key by private key:

```
from genesis_blockchain_tools.crypto import get_public_key

priv_key = '2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202'
pub_key = get_public_key(priv_key)
```

To sign message/data:

```
from genesis_blockchain_tools.crypto import sign

priv_key = '2922bee6973370915cc63ab5ab8b7a57e1cab909477d7a030b2e4661e7aa2202'
data = "Some data to sign"
signature = sign(priv_key, data)
```

Requirements
------------

Tested on Python 3 but should work on Python 2 also.
