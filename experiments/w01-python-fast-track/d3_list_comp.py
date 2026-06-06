# week1 - chapter 2
# array of sequences

# ============================================================
# 1. CONTAINER vs FLAT SEQUENCES — memory model
# ============================================================
# Container sequences (list, tuple, set, dict) store references (pointers) to objects
# Flat sequences(array.array, str, bytes) store raw C value inline - no pointer indirection, more compact and faster for large data

import array
import sys

container = [1.0, 2.0, 3.0]   # array of pointers to float objects
flat = array.array('d', [1.0, 2.0, 3.0]) 

# array.array is a module/class from Python's standard library that is somewhat similar to a C array or a std::vector<T> with a fixed element type.
# the first argument tells Python what type to store
# | Code  | Type          |
# | ----- | ------------- |
# | `'i'` | int           |
# | `'I'` | unsigned int  |
# | `'f'` | float         |
# | `'d'` | double        |
# | `'b'` | signed char   |
# | `'B'` | unsigned char |



big_list = [float(i) for i in range(100_000)]
big_array = array.array('d', (float(i) for i in range(100_000)))  # generator expression is more memory efficient than list comprehension for creating the array, because it doesn't create an intermediate list in memory.

print(sys.getsizeof(big_list))  # 800984 bytes (pointers + object overhead)
print(sys.getsizeof(big_array)) # 816640 bytes  (just raw doubles + small header)
# sys.getsizeof on list only counts the pointer array itself, not the pointed-to objects
# The real cost of big_list is much higher when you count all the float objects on the heap


# ============================================================
# 2. LIST COMPREHENSIONS — syntax and scope
# ============================================================
# Syntax: [expression for var in iterable if condition]
# The loop variable is LOCAL to the comprehension — gone after it finishes
# This was NOT the case in Python 2 (loop var leaked); Python 3 fixed it

symbols = '$¢£¥€¤'

# basic list comprehension
codes = [ord(s) for s in symbols]
print(codes)    #[36, 162, 163, 165, 8364, 164]

# with filter condition
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print(beyond_ascii) #[162, 163, 165, 8364, 164]

# nested comprehensions
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat_matrix = [x for row in matrix for x in row]
print(flat_matrix)      #[1, 2, 3, 4, 5, 6, 7, 8, 9]


colors = ['blacl', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)   #[('blacl', 'S'), ('blacl', 'M'), ('blacl', 'L'), ('white', 'S'), ('white', 'M'), ('white', 'L')]

# --- Walrus operator := inside a listcomp ---
# := assigns AND returns the value, and the assignment target leaks to the enclosing scope
# The loop variable does NOT leak
results = [last := ord(c) for c in 'ABC']
print(results)  # [65, 66, 67]
print(last)     # 67 — accessible after, because := leaks out
print(c)        # NameError — c is gone, it was the loop variable


# ============================================================
# 3. GENERATOR EXPRESSIONS (GENEXPS)
# ============================================================
# Same syntax as listcomp but enclosed in () instead of []
# Yields items one at a time — never builds the full list in memory
# Use when only need to iterate once, or feed into another constructor

# feed directly into array.array - no intermediate list created
arr = array.array('I', (ord(s) for s in symbols))
print(arr)   # array('I', [36, 162, 163, 165, 8364, 164])

# feed into tuple()
codes_tuple = tuple(ord(s) for s in symbols)
print(codes_tuple)  # (36, 162, 163, 165, 8364, 164)
# note: when genexp is the only argument, the extra () can be omitted

# sum() over a genexp - never creates the full list
total = sum(ord(s) for s in symbols)
print(total)  # 9054

# --- listcomp vs genexp mental model ---
# listcomp: builds entire list → [  ]  → hands it to caller
# genexp:   lazy iterator     → (  )  → yields one item at a time
# For large data (millions of items), genexp saves significant memory


# ============================================================
# 4. TUPLES — as records and as immutable lists
# ============================================================
# --- As records: position carries meaning ---
tokyo = ('Tokyo', 2003, 32_450, 0.66, 8)
city, year, pop, chg, area = tokyo   # unpacking — each position has a role
print(city, year)   # Tokyo 2003
 
# Iterate over a list of records
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for country, passport in sorted(traveler_ids):
    print(f'{country}/{passport}')
 
# --- As immutable lists: structural use ---
# tuple is slightly more compact than list
a = (1, 2, 3)
b = [1, 2, 3]
print(sys.getsizeof(a))  # 64 bytes
print(sys.getsizeof(b))  # 88 bytes
 
# Tuples with no mutable items are hashable → can be used as dict keys
locations = {(35.6, 139.7): 'Tokyo', (51.5, -0.1): 'London'}
print(locations[(35.6, 139.7)])   # 'Tokyo'
 
# --- The immutability trap ---
# Immutability applies to the REFERENCES, not the objects they point to
# The tuple cannot have references replaced, but mutable objects CAN be mutated
 
t = (1, 2, [3, 4])
# t[2] = [99]       # ❌ TypeError: tuple does not support item assignment
t[2].append(5)      # ✅ mutates the list object the reference points to
print(t)            # (1, 2, [3, 4, 5]) — tuple "changed"!
 
# Practical consequence: a tuple with a mutable element is NOT hashable
try:
    d = {t: 'value'}
except TypeError as e:
    print(e)    # unhashable type: 'list'
 
 
# ============================================================
# 5. UNPACKING ITERABLES
# ============================================================
 
# Basic unpacking — count must match exactly
a, b, c = (1, 2, 3)
 
# Swap without a temp variable — idiomatic Python
a, b = b, a
print(a, b)   # 2 1
 
# Star unpacking — collect remainder into a list
first, *rest         = [1, 2, 3, 4, 5]   # first=1,  rest=[2,3,4,5]
*head, last          = [1, 2, 3, 4, 5]   # head=[1,2,3,4], last=5
first, *middle, last = [1, 2, 3, 4, 5]   # first=1, middle=[2,3,4], last=5
print(first, middle, last)   # 1 [2, 3, 4] 5
 
# Star in function calls — unpack a list as positional args
def add(a, b, c): return a + b + c
args = [1, 2, 3]
print(add(*args))   # 6
 
# Nested unpacking
(a, b), c = (1, 2), 3
print(a, b, c)   # 1 2 3
 
# Practical: ignore values with _
_, month, _ = (2026, 6, 1)   # only care about month
print(month)   # 6
 
 
# ============================================================
# 6. SLICING
# ============================================================
# seq[start:stop:step]
# stop is EXCLUSIVE — seq[1:4] gives indices 1, 2, 3 (not 4)
# Negative step reverses direction
 
s = 'bicycle'
print(s[::3])    # 'bye'      — every 3rd character
print(s[::-1])   # 'elcycib'  — reversed
print(s[-3:])    # 'cle'      — last 3 characters
 
l = list(range(10))   # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 
# Slice assignment — mutable sequences only, length of replacement can differ
l[2:5] = [20, 30]    # replace 3 elements with 2
print(l)             # [0, 1, 20, 30, 5, 6, 7, 8, 9]
 
del l[5:7]           # delete a section
print(l)             # [0, 1, 20, 30, 5, 9]
 
# --- Named slices — interview-worthy pattern ---
# In fixed-width record parsing, magic numbers scattered everywhere are unreadable
# Named slices make the intent explicit and the code maintainable
 
# Simulated fixed-width data record (like a legacy database export)
record = "2026-06-01  MSFT        350.25   BUY "
#         0123456789  10        20        30
 
DATE   = slice(0, 10)
TICKER = slice(12, 16)
PRICE  = slice(20, 26)
ACTION = slice(29, 32)
 
print(record[DATE].strip())    # '2026-06-01'
print(record[TICKER].strip())  # 'MSFT'
print(record[PRICE].strip())   # '350.25'
print(record[ACTION].strip())  # 'BUY'
 
 
# ============================================================
# 7. list.sort() vs sorted()
# ============================================================
# list.sort()  — in-place, modifies the list, returns None
# sorted()     — returns a NEW list, works on any iterable, original unchanged
 
fruits = ['grape', 'raspberry', 'apple', 'banana']
 
# sorted() — non-destructive
print(sorted(fruits))                    # ['apple', 'banana', 'grape', 'raspberry']
print(sorted(fruits, reverse=True))      # ['raspberry', 'grape', 'banana', 'apple']
print(sorted(fruits, key=len))           # ['grape', 'apple', 'banana', 'raspberry']
print(fruits)                            # ['grape', 'raspberry', 'apple', 'banana'] — unchanged
 
# list.sort() — in-place
fruits.sort()
print(fruits)   # ['apple', 'banana', 'grape', 'raspberry'] — modified in place
 
# --- The None trap ---
# list.sort() returns None — this is a Python convention signaling in-place mutation
# Never assign it
result = fruits.sort()
print(result)   # None  ← you just lost your reference to the sorted list
 
# Two-key sort using a tuple key — sort by length, then alphabetically
words = ['fig', 'apple', 'banana', 'kiwi', 'pear']
print(sorted(words, key=lambda w: (len(w), w)))
# ['fig', 'kiwi', 'pear', 'apple', 'banana']
# Within same length: alphabetical order applies
 
 
# ============================================================
# QUICK EXERCISE SOLUTIONS
# ============================================================
 
# a) Rotate a list left by n using slicing only
def rotate_left(lst: list, n: int) -> list:
    n = n % len(lst)          # handle n > len
    return lst[n:] + lst[:n]
 
print(rotate_left([1,2,3,4,5], 2))   # [3, 4, 5, 1, 2]
 
# b) Remove duplicates preserving order (no set() directly on list)
def dedupe(lst: list) -> list:
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]
    # seen.add() returns None (falsy), so 'seen.add(x) or x in seen' pattern works
 
print(dedupe([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))   # [3, 1, 4, 5, 9, 2, 6]
 
# c) Zip two lists into a dict using a listcomp
keys   = ['a', 'b', 'c']
values = [1, 2, 3]
d = {k: v for k, v in zip(keys, values)}
print(d)   # {'a': 1, 'b': 2, 'c': 3}
 
# d) Transpose a matrix with a listcomp
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
print(transposed)
# [[1, 4, 7],
#  [2, 5, 8],
#  [3, 6, 9]]
# Or more idiomatically: list(map(list, zip(*matrix)))
 