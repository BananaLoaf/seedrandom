# seedrandom
Random number generation based on the seed

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

### Is it random?

Uppon generating 100000 random numbers in a range of 1 to 5, it showed equal distribution

|       |           |
|---	|:-----:	|
| 1 	| 20.0% 	|
| 2 	| 20.2% 	|
| 3 	| 19.9% 	|
| 4 	| 20.0% 	|
| 5 	| 19.9% 	|

### Usage

```python
from seedrandom import Seed
seed = Seed(b"Test", b"values")
```

Generating random values:
```python
seed.randint(_min=1, _max=10)
seed.randfloat(_min=0, _max=6, step=0.1)
seed.randbool()
seed.randbyte()
```

```Seed``` can be converted to and from ```int``` or ```bytes```:
```python
seed1 = Seed(b"Bytes")
seed2 = Seed(b"Int")
bytes(seed1)  # b"\x9e^\n\x06j\x99\xe1`\x86m-\xe7Z\n\xbdSN\x92O}\x89@\xd0\r'\x86\xf1\xaf\xcd\xd4\xa2'"
int(seed2)  # 31431599345838686137398213930967341686259486292204322755690725188121734625692

seed1 = Seed.from_bytes(b"\x9e^\n\x06j\x99\xe1`\x86m-\xe7Z\n\xbdSN\x92O}\x89@\xd0\r'\x86\xf1\xaf\xcd\xd4\xa2'")  # <seedrandom.Seed object at 0x0000002CA1D7F8D0>
seed2 = Seed.from_int(31431599345838686137398213930967341686259486292204322755690725188121734625692)  # <seedrandom.Seed object at 0x0000002CA1D7F9B0>
```

```Seed``` can use different hashing functions from ```hashlib``` module
```python
seed1 = Seed(b"Test", b"values")  # Uses hashlib.sha256 by default
seed2 = Seed(b"Test", b"values", hash_func=hashlib.md5)

seed1.randint(_min=0, _max=100000)  # 2457
seed2.randint(_min=0, _max=100000)  # 98655
```

```ordered``` argument can be used:
```python
seed1 = Seed(b"Hello", b"world")
seed2 = Seed(b"world", b"Hello")
seed1 == seed2  # True

seed1 = Seed(ordered=(b"Hello", b"world"))
seed2 = Seed(ordered=(b"world", b"Hello"))
seed1 == seed2  # False

seed1 = Seed(b"Hello", b"world", ordered=(b"spanish", b"inquisition"))
seed2 = Seed(b"world", b"Hello", ordered=(b"spanish", b"inquisition"))
seed1 == seed2  # True

seed1 = Seed(b"Hello", b"world", ordered=(b"spanish", b"inquisition"))
seed2 = Seed(b"Hello", b"world", ordered=(b"inquisition", b"spanish"))
seed1 == seed2  # False
```
