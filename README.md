# seedrandom
Deterministic seeded RNG

[![Python Version](https://img.shields.io/pypi/pyversions/seedrandom.svg?color=yellow&style=flat-square)](https://www.python.org/downloads/)
[![GitHub Licence](https://img.shields.io/github/license/BananaLoaf/seedrandom.svg?color=blue&style=flat-square)](https://github.com/BananaLoaf/seedrandom/blob/master/LICENSE)
[![Package Version](https://img.shields.io/pypi/v/seedrandom.svg?color=green&style=flat-square)](https://pypi.org/project/seedrandom/)


### Installation / Updating
```
pip install seedrandom
pip install --upgrade seedrandom
```
Or
```
pip install git+https://github.com/BananaLoaf/seedrandom.git
pip install --upgrade git+https://github.com/BananaLoaf/seedrandom.git
```

### Usage

```python
from seedrandom import SeededRNG
rng = SeededRNG(b"Test", b"values", hash_func=hashlib.sha512)  # any hash func from hashlib
```

Generating random values:
```python
rng.randint(a=0, b=1000)  # 893
rng.randfloat(a=0, b=100, step=0.1)  # 89.3
rng.randbool()  # False
rng.randbyte()  # b'\xbf'
```

```SeededRNG``` can be converted to and from ```int``` or ```bytes```:
```python
bytes(rng)
int(rng)

rng1 = SeededRNG.from_bytes(b'\xbb\x9a\xf3\xe3\x1d\xfcA\xcc\xc5\x93S\x9a\xec:\x9a\x08z\x88\x85\x99\xf7\xea\x91\xb6x\x00\xfb\x82"\xc2$K', hash_func=hashlib.blake2s)
rng2 = SeededRNG.from_int(13391421701272821393603640485300504071883816826531413055648909144818643814535822212998295950921452703111178763035507290455800978052021014498426299707601814, hash_func=hashlib.sha512)
```

```ordered``` parameter can be used:
```python
rng1 = SeededRNG(b"Hello", b"world")
rng2 = SeededRNG(b"world", b"Hello")
rng1 == rng2  # True

rng1 = SeededRNG(ordered=(b"Hello", b"world"))
rng2 = SeededRNG(ordered=(b"world", b"Hello"))
rng1 == rng2  # False

rng1 = SeededRNG(b"Hello", b"world", ordered=(b"spanish", b"inquisition"))
rng2 = SeededRNG(b"world", b"Hello", ordered=(b"spanish", b"inquisition"))
rng1 == rng2  # True

rng1 = SeededRNG(b"Hello", b"world", ordered=(b"spanish", b"inquisition"))
rng2 = SeededRNG(b"Hello", b"world", ordered=(b"inquisition", b"spanish"))
rng1 == rng2  # False
```
