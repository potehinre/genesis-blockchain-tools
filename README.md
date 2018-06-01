Genesis BlockChain Tools
========================

Setup
-----

## Prerequisites:

Currenty four cryptographic backend modules are supported:
* [python-ecdsa](https://github.com/warner/python-ecdsa)
* [ECPy](http://ubinity.github.io/ECPy/)
* [fastecdsa](https://github.com/AntonKueltz/fastecdsa)
* [rubenesque](https://github.com/latchset/python-rubenesque)

### Setting up python-ecdsa

python-ecdsa is pure python implementation of ECDSA. Use this module if you have issues with dependencies installation (on Windows for exapmle):

```
pip install ecdsa
```

### Setting up ECPy

ECPy is pure python implementation of ECDSA. Use this module if you have issues with dependencies installation (on Windows for exapmle):

```
pip install ECPy
```

### Setting up fastecdsa

fastecdsa is C/C++ module. It's the fastest between others. Use this module if you have no issues with dependencies (on Debian/Ubuntu Linux for example):

```
pip install fastecdsa
```

### Setting up rubenesque

rubenesque is pure python implementaion of ECDSA also. But it's not on PyPI. So if you want to use it you have to install it from github repository directly:

```
pip install git+https://github.com/latchset/python-rubenesque
```

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

Tested on Python 3.x only yet
