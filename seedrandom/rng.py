"""Deterministic random number generator."""

import hashlib
from typing import Callable, Optional, Union

DEFAULT_HASH_FUNC = hashlib.md5


class SeededRNG(object):  # noqa: WPS338
    """Deterministic random number generator."""

    def __init__(
        self,
        *unordered,
        ordered: Optional[Union[tuple, list]] = None,
        hash_func: Callable = DEFAULT_HASH_FUNC,
    ):
        if ordered is None:
            ordered = ()

        for elem in unordered + tuple(ordered):
            if not isinstance(elem, bytes):
                raise TypeError('All elements must be bytes')

        if hash_func.__module__ not in {'_hashlib', '_blake2'}:
            raise TypeError('Unrecognized hash function')

        self._source = (unordered, tuple(ordered))
        self._hash_func = hash_func
        self._digest_size = hash_func().digest_size
        self._seed = self._generate(
            unordered=unordered,
            ordered=tuple(ordered),
        )

    def _generate(self, unordered: tuple, ordered: tuple) -> bytes:
        unordered = list(unordered)
        ordered = list(ordered)

        if len(unordered) == 0 and len(ordered) == 0:
            return b'\x00' * self._digest_size

        if len(unordered) > 0:
            for itr, elem in enumerate(unordered):
                # Hash bytes and replace
                unordered[itr] = self._hash_func(elem).digest()

            # Sort unordered list by integer representation of each hash from
            # lowest to highest
            unordered.sort(key=lambda x: int.from_bytes(x, byteorder='big'))  # noqa: WPS111 E501

        if len(ordered) > 0:
            for itr, elem in enumerate(ordered):
                # Hash and replace
                ordered[itr] = self._hash_func(elem).digest()

        # Same as to merge hashes into one string and return its hash
        hasher = self._hash_func()
        for elem in unordered + ordered:
            hasher.update(elem)
        return hasher.digest()

    ################################################################
    def __bytes__(self):
        return self._seed

    def __int__(self):
        return int.from_bytes(self._seed, byteorder='big')

    def __eq__(self, other):
        if isinstance(other, SeededRNG):
            return self._seed == other._seed  # noqa: WPS437

        elif isinstance(other, bytes):
            return bytes(self) == other

        elif isinstance(other, int):
            return int(self) == other

        return NotImplemented

    def __hash__(self):
        return int(self)

    ################################################################
    @classmethod
    def from_bytes(
        cls,
        byte_data: bytes,
        hash_func: Callable = DEFAULT_HASH_FUNC,
    ):
        """Create class from bytes."""
        if len(byte_data) != hash_func().digest_size:
            raise ValueError('Size of byte_data does not match output size for specified hash function')  # noqa: E501
        instance = cls(hash_func=hash_func)
        instance._seed = byte_data  # noqa: WPS437
        return instance

    @classmethod
    def from_int(cls, int_data: int, hash_func: Callable = DEFAULT_HASH_FUNC):
        """Create class from int."""
        try:
            byte_data = int_data.to_bytes(
                hash_func().digest_size,
                byteorder='big',
            )
        except OverflowError:
            raise OverflowError('int too big to convert for given hash_func')
        return cls.from_bytes(byte_data, hash_func=hash_func)

    ################################################################
    def randint(self, a: int, b: int) -> int:  # noqa: WPS111
        """Random int value in range [a, b]."""
        if a > b:
            raise ValueError('a can not be more than b')
        return a + int(self) % (b - a + 1)

    def randfloat(self, a: float, b: float, step: float = 0.1) -> float:  # noqa: WPS111 E501
        """Random float value in range [a, b] with specified step."""
        if a > b:
            raise ValueError('a can not be more than b')
        if step < 0:
            raise ValueError('step less than 0')

        # How many possible entries are there
        num_of_entries = int((b - a) / step) + 1
        # Picking a random entry
        entry = int(self) % num_of_entries
        # Calc value at an entry and round it in an awful way
        return round(a + step * entry, len(str(step).split('.')[1]))  # noqa: WPS221 E501

    def randbool(self) -> bool:
        """Get random bool."""
        return [True, False][int(self) % 2]

    def randbyte(self) -> bytes:
        """Get random byte."""
        return bytes([self.randint(a=0, b=255)])  # noqa: WPS432
