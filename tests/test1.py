from seedrandom import Seed


def pretty(val: bool) -> str:
    return "Passed" if val else "Failed"


if __name__ == "__main__":
    seed = Seed(b"Test")
    print("Performing tests...")
    print("To bytes:\t\t\t", pretty(bytes(seed) == b"\xc6\t\x07\xe9\x90t_}\x91\xc4B7\x13vM'$W\x12i\xd3\xdbHV\xd3|c\x02y,Y\xa6"))
    print("To int:\t\t\t\t", pretty(int(seed) == 89573900252174594416690676482213085989859255220914121309760993229094666394022))
    print("From bytes:\t\t\t", pretty(seed == Seed.from_bytes(bytes(seed))))
    print("From int:\t\t\t", pretty(seed == Seed.from_int(int(seed))))
    print()
    print("Eq seed to bytes:\t", pretty(seed == b"\xc6\t\x07\xe9\x90t_}\x91\xc4B7\x13vM'$W\x12i\xd3\xdbHV\xd3|c\x02y,Y\xa6"))
    print("Eq seed to int:\t\t", pretty(seed == 89573900252174594416690676482213085989859255220914121309760993229094666394022))
    print("Eq seed to seed:\t", pretty(seed == Seed(b"Test")))
    print()
    print("Rand int:\t\t\t", pretty(seed.randint(_min=0, _max=100) == 88))
    print("Rand float:\t\t\t", pretty(seed.randfloat(_min=0, _max=10, step=0.1) == 8.8))
    print("Rand bool:\t\t\t", pretty(seed.randbool() is True))
    print("Rand byte:\t\t\t", pretty(seed.randbyte() == b"\xa6"))
    print()
    seed1 = Seed(b"First", b"Second")
    seed2 = Seed(b"Second", b"First")
    print("Unordered:\t\t\t", pretty(seed1 == seed2))
    seed1 = Seed(b"First", b"Second", ordered=[b"First_ordered", b"Second_ordered"])
    seed2 = Seed(b"First", b"Second", ordered=[b"Second_ordered", b"First_ordered"])
    print("Ordered:\t\t\t", pretty(seed1 != seed2))
    print()
