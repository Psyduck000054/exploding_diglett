import math
from hash import get_string_segment

# "rng" that is predetermined using seedstring manipulation
class temu_rng:
    def __init__(self, seed_int):
        self.seed_string = get_string_segment(seed_int, 0, 1048576)
        self.pointer = 0
        self.length_limit = len(self.seed_string)

    # get a part of the seedstring with given length
    def _get_chunk(self, length):
        if self.pointer + length > self.length_limit:
            self.pointer = 0
            
        chunk = self.seed_string[self.pointer : self.pointer + length]
        self.pointer += length
        return int(chunk)

    def random(self):
        value = self._get_chunk(5)
        return value / 100000.0

    def randint(self, a, b):
        span = b - a + 1
        value = self._get_chunk(5)
        return a + (value % span)

    def choice(self, sequence):
        if not sequence:
            return None
        index = self.randint(0, len(sequence) - 1)
        return sequence[index]