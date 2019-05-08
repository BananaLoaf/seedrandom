import hashlib

__version__ = "1.4"
SEED_LEN = 64


class Seed:
    def __init__(self, *source, ordered: list = [], hash_func=hashlib.sha256):
        if len(source) == 0 and len(ordered) == 0:
            raise AttributeError("arguments missing")
        if callable(hash_func):
            if hasattr(hash_func(), "digest"):
                if not isinstance(hash_func().digest(), bytes):
                    raise TypeError("digest() method has to return bytes")
            else:
                raise AttributeError("hash_func() has no digest() method")
        else:
            hash_func()

        self._hash_func = hash_func
        self._source = (source, ordered)
        self.seed = self._generate(*source, ordered=ordered, hash_func=hash_func)

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        self._seed = b"\x00"*(SEED_LEN - len(value)) + value

    @seed.getter
    def seed(self) -> bytes:
        return self._seed.lstrip(b"\x00")

    @staticmethod
    def _generate(*source, ordered: list = [], hash_func=None) -> bytes:
        """Generates seed bytes from source bytes"""
        if source or ordered:
            if ordered:
                for i, elem in enumerate(ordered):
                    # Check types
                    if not isinstance(elem, bytes):
                        raise TypeError(f"Non bytes type of '{elem}' is not supported")
                    # Hash bytes and replace
                    ordered[i] = hash_func(elem).digest()
            else:
                ordered = []

            if source:
                unordered = list(source)
                for i, elem in enumerate(unordered):
                    # Check types
                    if not isinstance(elem, bytes):
                        raise TypeError(f"Non bytes type of '{elem}' is not supported")
                    # Hash bytes and replace
                    unordered[i] = hash_func(elem).digest()

                # Sort unordered list by integer representation of each hash from lowest to highest
                unordered.sort(key=lambda data: int.from_bytes(data, byteorder='big'))
            else:
                unordered = []

            # Merge hashes into one string ordered first unordered second and return it's hash
            merged = b"".join(ordered + unordered)
            return hash_func(merged).digest()
        else:
            return b"\x00" * SEED_LEN

    def randint(self, _max: int, _min: int = 0) -> int:
        """Random int value in range [_min, _max]"""
        if _min > _max:
            raise ValueError("_min can not be bigger than _max")

        return _min + int(self) % (_max - _min + 1)

    def randfloat(self, _max: float, _min: float = 0, step: float = 0.1) -> float:
        """Random float value in range [_min, _max] with specified step"""
        if _min > _max:
            raise ValueError("_min can not be bigger than _max")
        if step <= 0:
            raise ValueError("Step can not be less or equal to 0")

        num_of_entries = int((_max - _min)/step + 1)  # now many possible entries are there
        entry = int(self) % num_of_entries  # picking the entry
        return round(_min + step * entry, len(str(step).split(".")))  # calc value at entry, shift it and round it in an awful way

    def randbool(self) -> bool:
        """Random bool value"""
        return [True, False][int(self) % 2]

    def randbyte(self) -> bytes:
        """Random byte"""
        return bytes([self.randint(_min=0, _max=255)])

    @classmethod
    def from_bytes(cls, byte_data: bytes):
        """Return Seed from user specified bytes"""
        obj = cls(b"")
        obj.seed = byte_data
        return obj

    @classmethod
    def from_int(cls, int_data: int):
        """Return Seed from user specified int value"""
        byte_data = int_data.to_bytes(SEED_LEN, byteorder="big")
        return cls.from_bytes(byte_data)

    def __bytes__(self):
        return self.seed

    def __int__(self):
        return int.from_bytes(self.seed, byteorder="big")

    def __eq__(self, other):
        if isinstance(other, Seed):
            return self.seed == other.seed
        elif isinstance(other, bytes):
            return bytes(self) == other
        elif isinstance(other, int):
            return int(self) == other
        else:
            return NotImplemented
