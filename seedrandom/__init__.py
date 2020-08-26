import hashlib
from typing import Optional, Callable, Union

PACKAGE_NAME = "seedrandom"
__version__ = "2.2.1"

DEFAULT_HASH_FUNC = hashlib.md5


class SeededRNG:
    def __init__(self, *unordered, ordered: Optional[Union[tuple, list]] = None, hash_func: Callable = DEFAULT_HASH_FUNC):
        if ordered is None:
            ordered = ()

        for elem in unordered + tuple(ordered):
            assert isinstance(elem, bytes), "All elements must be bytes"

        assert hash_func.__module__ in ["_hashlib", "_blake2"]

        self._source = (unordered, tuple(ordered))
        self._hash_func = hash_func
        self._digest_size = hash_func().digest_size
        self._seed = self._generate(unordered=unordered, ordered=tuple(ordered))

    def _generate(self, unordered: tuple, ordered: tuple) -> bytes:
        unordered = list(unordered)
        ordered = list(ordered)

        if len(unordered) == 0 and len(ordered) == 0:
            return b"\x00" * self._digest_size

        if len(unordered) > 0:
            for i, elem in enumerate(unordered):
                # Hash bytes and replace
                unordered[i] = self._hash_func(elem).digest()

            # Sort unordered list by integer representation of each hash from lowest to highest
            unordered.sort(key=lambda x: int.from_bytes(x, byteorder="big"))

        if len(ordered) > 0:
            for i, elem in enumerate(ordered):
                # Hash and replace
                ordered[i] = self._hash_func(elem).digest()

        # Same as to merge hashes into one string and return its hash
        h = self._hash_func()
        for elem in unordered + ordered:
            h.update(elem)
        return h.digest()

    ################################################################
    def __bytes__(self):
        return self._seed

    def __int__(self):
        return int.from_bytes(self._seed, byteorder="big")

    def __eq__(self, other):
        if isinstance(other, SeededRNG):
            return self._seed == other._seed

        elif isinstance(other, bytes):
            return bytes(self) == other

        elif isinstance(other, int):
            return int(self) == other

        else:
            return NotImplemented

    def __hash__(self):
        return int(self)

    ################################################################
    @classmethod
    def from_bytes(cls, byte_data: bytes, hash_func: Callable = DEFAULT_HASH_FUNC):
        """
        :return: SeededRNG
        """
        assert len(byte_data) == hash_func().digest_size
        self = cls(hash_func=hash_func)
        self._seed = byte_data
        return self

    @classmethod
    def from_int(cls, int_data: int, hash_func: Callable = DEFAULT_HASH_FUNC):
        """
        :return: SeededRNG
        """
        try:
            byte_data = int_data.to_bytes(hash_func().digest_size, byteorder="big")
        except OverflowError:
            raise OverflowError("int too big to convert for given hash_func")
        return cls.from_bytes(byte_data, hash_func=hash_func)

    ################################################################
    def randint(self, a: int, b: int) -> int:
        """Random int value in range [a, b]"""
        assert b > a
        return a + int(self) % (b - a + 1)

    def randfloat(self, a: float, b: float, step: float = 0.1) -> float:
        """Random float value in range [a, b] with specified step"""
        assert b > a
        assert step > 0

        num_of_entries = int((b - a) / step) + 1  # How many possible entries are there
        entry = int(self) % num_of_entries  # Picking a random entry
        return round(a + step * entry, len(str(step).split(".")[1]))  # Calc value at an entry and round it in an awful way

    def randbool(self) -> bool:
        return [True, False][int(self) % 2]

    def randbyte(self) -> bytes:
        return bytes([self.randint(a=0, b=255)])
