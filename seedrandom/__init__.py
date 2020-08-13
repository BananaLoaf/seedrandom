import hashlib
from typing import Optional, Callable

__version__ = "1.4.1"

DEFAULT_HASH_FUNC = hashlib.md5


class SeededRNG:
    def __init__(self, *unordered, ordered: Optional[list] = None, hash_func: Callable = DEFAULT_HASH_FUNC):
        if ordered is None:
            ordered = []

        for elem in list(unordered) + ordered:
            assert isinstance(elem, bytes), "All elements must be bytes"

        assert hash_func.__module__ in ["_hashlib", "_blake2"]

        self._source = (unordered, tuple(ordered))
        self._hash_func = hash_func
        self._digest_size = hash_func().digest_size
        self._seed = self._generate(unordered=list(unordered), ordered=ordered)

    def _generate(self, unordered: list, ordered: list) -> bytes:
        if len(unordered) == 0 and len(ordered) == 0:
            return b"\x00" * self._digest_size

        if len(ordered) > 0:
            for i, elem in enumerate(ordered):
                # Hash and replace
                ordered[i] = self._hash_func(elem).digest()

        if len(unordered) > 0:
            for i, elem in enumerate(unordered):
                # Hash bytes and replace
                unordered[i] = self._hash_func(elem).digest()

            # Sort unordered list by integer representation of each hash from lowest to highest
            unordered.sort(key=lambda x: int.from_bytes(x, byteorder="big"))

        # Merge hashes into one string ordered first unordered second and return its hash
        merged = b"".join(ordered + unordered)
        return self._hash_func(merged).digest()

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
    def randint(self, max: int, min: int = 0) -> int:
        """Random int value in range [min, max]"""
        assert max > min
        return min + int(self) % (max - min + 1)  # TODO max - 1

    def randfloat(self, max: float, min: float = 0, step: float = 0.1) -> float:
        """Random float value in range [min, max] with specified step"""
        assert max > min
        assert step > 0

        num_of_entries = int((max - min) / step) + 1  # How many possible entries are there
        entry = int(self) % num_of_entries  # Picking the random entry
        return round(min + step * entry, len(str(step).split(".")[1]))  # Calc value at entry and round it in an awful way

    def randbool(self) -> bool:
        return [True, False][int(self) % 2]

    def randbyte(self) -> bytes:
        return bytes([self.randint(min=0, max=255)])


if __name__ == '__main__':
    seed2 = SeededRNG(b"Test")
    print(bytes(seed2))
    print(int(seed2))