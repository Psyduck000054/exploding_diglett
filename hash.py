import hashlib
import struct
from constants import *
import random

def get_string_segment(seed, start_index, length):
    full_digits = []
    block_index = 0 
    
    while len(full_digits) < start_index + length:
        input_data = struct.pack('>qQ', seed, block_index)
        digest_bytes = hashlib.sha256(input_data).digest()
        
        # remove items >= 250 so each digits has exactly 25 occurrences
        for b in digest_bytes:
            if b < 250:
                full_digits.append(str(b % 10))
                
        block_index += 1

    large_string = "".join(full_digits)
    
    return large_string[start_index : start_index + length]

# get seed val
def get_seed_val (seedstring, pointer, length):
    if length > 32:
        return "int too long"
    temp = pointer
    pointer += length
    return int(seedstring[temp:(temp + length)])