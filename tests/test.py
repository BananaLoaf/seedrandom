from seedrandom import SeededRNG
import hashlib


seed = SeededRNG(b"Test", hash_func=hashlib.sha256)
seed_bytes = b"\xc6\t\x07\xe9\x90t_}\x91\xc4B7\x13vM'$W\x12i\xd3\xdbHV\xd3|c\x02y,Y\xa6"
seed_int = 89573900252174594416690676482213085989859255220914121309760993229094666394022


def test_to_bytes():
    assert bytes(seed) == seed_bytes


def test_to_int():
    assert int(seed) == seed_int


def test_eq_seed():
    assert seed == SeededRNG(b"Test", hash_func=hashlib.sha256)


def test_eq_bytes():
    assert seed == seed_bytes


def test_eq_int():
    assert seed == seed_int


################################################################
def test_from_bytes():
    assert seed == SeededRNG.from_bytes(seed_bytes, hash_func=hashlib.sha256)


def test_from_int():
    assert seed == SeededRNG.from_int(seed_int, hash_func=hashlib.sha256)


################################################################
def test_randint():
    assert seed.randint(min=0, max=100) == 88


def test_randfloat():
    assert seed.randfloat(min=0, max=10, step=0.1) == 8.8


def test_randbool():
    assert seed.randbool() is True


def test_randbyte():
    assert seed.randbyte() == b"\xa6"


################################################################
def test_unordered():
    seed1 = SeededRNG(b"First", b"Second", hash_func=hashlib.sha256)
    seed2 = SeededRNG(b"Second", b"First", hash_func=hashlib.sha256)
    assert seed1 == seed2


def test_ordered():
    seed1 = SeededRNG(ordered=[b"First_ordered", b"Second_ordered"], hash_func=hashlib.sha256)
    seed2 = SeededRNG(ordered=[b"Second_ordered", b"First_ordered"], hash_func=hashlib.sha256)
    assert seed1 != seed2

    seed1 = SeededRNG(b"First", b"Second", ordered=[b"First_ordered", b"Second_ordered"], hash_func=hashlib.sha256)
    seed2 = SeededRNG(b"First", b"Second", ordered=[b"Second_ordered", b"First_ordered"], hash_func=hashlib.sha256)
    assert seed1 != seed2


def test_zeros():
    assert SeededRNG(hash_func=hashlib.sha256)._seed == hashlib.sha256().digest_size * b"\x00"
