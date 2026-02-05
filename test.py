from hash import *
import random
from constants import *

seed = random.randint(INT64_MIN, INT64_MAX)
seedstring = get_string_segment(seed, 0, 100)

print (seed)
print (seedstring)