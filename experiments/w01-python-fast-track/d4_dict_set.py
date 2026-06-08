# week1 - chapter 3
# dictionaries and sets
 
 
# ============================================================
# 1. WAYS TO CREATE A DICT
# ============================================================
# 1. literal
d1 = {'a': 1, 'b': 2, 'c': 3}

# 2. dict() with keyword args - keys must be valid identifiers
d2 = dict(a=1, b=2, c=3)

# 3. dict() from iterable of key-value pairs
d3 = dict([('a', 1), ('b', 2), ('c', 3)])

# 4. dict() + zip - pair two sepate iterables together
d4 = dict(zip(['a', 'b', 'c'], [1, 2, 3]))

# 5. fromkeys - all keys initialized to same value
d5 = dict.fromkeys(['a', 'b', 'c'], 0)

print(d1 == d2 == d3 == d4)  # True

# --- fromkeys mutable default trap ---
# all keys share the same list object, so mutating one mutates them all
bad = dict.fromkeys(['a', 'b', 'c'], [])
print(bad) # {'a': [], 'b': [], 'c': []}
bad['a'].append(1)
print(bad) # {'a': [1], 'b': [1], 'c': [1]}

# dict comprehension - create dict gives each key its own object
good = {k: [] for k in ['a', 'b', 'c']}
print(good) # {'a': [], 'b': [], 'c': []}
good['a'].append(1)
print(good) # {'a': [1], 'b': [], 'c': []}


# ============================================================
# 2. DICT COMPREHENSIONS
# ============================================================
# syntax: {key_expr: value_expr for var in iterable if condition}
# builds a new dict from any iterables - key:value pairs

# basic example - swap keys and values
dial_code = [('US', 1), ('UK', 44), ('India', 91)]
code_to_country = {code: country for country, code in dial_code}
print(code_to_country) # {1: 'US', 44: 'UK', 91: 'India'}

# with filter
larger_code = {code: country for country, code in dial_code if code > 50}
print(larger_code) # {91: 'India'}

# invert an existing dict
original = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in original.items()}
print(inverted) # {1: 'a', 2: 'b', 3: 'c'}
# only safe if values are unique and hashable


# ============================================================
# 3. MERGING MAPPINGS — | and |=
# ============================================================
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}
 
# | creates a NEW merged dict — d1 and d2 unchanged
merged = d1 | d2
print(merged)   # {'a': 1, 'b': 3, 'c': 4}
print(d1)       # {'a': 1, 'b': 2}  — untouched
# Rightmost wins on conflict: d2's 'b': 3 overwrites d1's 'b': 2
 
# |= updates IN-PLACE (augmented assignment)
d1 |= d2
print(d1)       # {'a': 1, 'b': 3, 'c': 4}  — d1 modified
 
# Pre-3.9 equivalent — still common in real codebases
d1 = {'a': 1, 'b': 2}
merged_old = {**d1, **d2}   # same semantics as d1 | d2
print(merged_old)   # {'a': 1, 'b': 3, 'c': 4}
 
# ⚠️ update() merges in-place but returns None — never assign it
result = d1.update(d2)
print(result)   # None  ← lost the dict reference
 
 
# ============================================================
# 4. PATTERN MATCHING WITH MAPPINGS
# ============================================================
# Dict patterns are PARTIAL — extra keys in the subject are ignored
# Only the specified keys need to be present for a match
 
def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            # [*names]: value must be a list; all elements captured into names
            return names
 
        case {'type': 'book', 'api': 1, 'author': str(name)}:
            # str(name): type-checks AND binds — only matches if value is a str
            return [name]
 
        case {'type': 'book', 'api': 1, 'author': name}:
            # bare name: matches ANY value for 'author', no type check
            return [name]
 
        case {'type': 'book'}:
            raise ValueError(f"Invalid book record: {record}")
 
        case {'type': 'movie', 'director': str(name)}:
            return [name]
 
        case _:
            raise ValueError(f"Unknown record: {record}")
 
print(get_creators({'type': 'book', 'api': 2, 'authors': ['Alice', 'Bob']}))
# ['Alice', 'Bob']
 
print(get_creators({'type': 'book', 'api': 1, 'author': 'Carol', 'isbn': '123'}))
# ['Carol'] — 'isbn' is extra, ignored by the partial match
 
print(get_creators({'type': 'movie', 'director': 'Nolan', 'year': 2023}))
# ['Nolan']
 
 
# ============================================================
# 5. STANDARD API — READ, WRITE, DEFAULT HANDLING
# ============================================================
d = {'a': 1, 'b': 2, 'c': 3}
 
# --- Read ---
print(d['a'])          # 1  — KeyError if missing
print(d.get('z'))      # None — safe
print(d.get('z', 0))   # 0   — with default
 
# Membership — O(1) hash lookup, same speed as set
print('a' in d)        # True
print('z' not in d)    # True
 
# --- Write ---
d['z'] = 99            # insert or update
del d['a']             # KeyError if absent
print(d)               # {'b': 2, 'c': 3, 'z': 99}
 
# --- setdefault: insert-if-absent + return in ONE lookup ---
# Use case: building an inverted index (word → list of positions)
text = 'the cat sat on the mat the cat'
index = {}
for pos, word in enumerate(text.split()):
    index.setdefault(word, []).append(pos)
print(index)
# {'the': [0, 4, 6], 'cat': [1, 7], 'sat': [2], 'on': [3], 'mat': [5]}
 
# Anti-pattern — two separate lookups:
# if word not in index:
#     index[word] = []
# index[word].append(pos)
 
# --- defaultdict: auto-creates missing keys via a factory ---
from collections import defaultdict
 
# Same inverted index, cleaner with defaultdict
index2: defaultdict[str, list] = defaultdict(list)
for pos, word in enumerate(text.split()):
    index2[word].append(pos)   # no KeyError — list() called automatically on first access
print(dict(index2))   # same result as above
 
# ⚠️ defaultdict factory must be a CALLABLE, not a value
# defaultdict(list)    ✅ — list() called per missing key
# defaultdict(list())  ❌ — [] passed as factory, not callable → TypeError on access
# defaultdict(0)       ❌ — int 0 is not callable
# defaultdict(int)     ✅ — int() returns 0, useful for counters
 
counter = defaultdict(int)
for word in text.split():
    counter[word] += 1
print(dict(counter))   # {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}
 
 
# ============================================================
# 6. COMMON MAPPING METHODS
# ============================================================
d = {'a': 1, 'b': 2, 'c': 3}
 
# pop — remove and return, KeyError if absent without default
val = d.pop('a')           # val = 1
safe = d.pop('z', None)    # None — no error
 
# popitem — removes and returns LAST inserted (key, value) pair — LIFO
# (not random — this surprises people)
d['x'] = 10
print(d.popitem())   # ('x', 10) — last inserted
 
# copy — shallow copy (nested objects still shared)
import copy
original = {'a': [1, 2], 'b': 3}
shallow = original.copy()
deep    = copy.deepcopy(original)
 
shallow['a'].append(99)
print(original['a'])   # [1, 2, 99] — shared! shallow copy didn't duplicate the list
print(deep['a'])       # [1, 2]     — fully independent
 
# Insertion order guaranteed since Python 3.7
d = {'b': 2, 'a': 1, 'c': 3}
print(list(d.keys()))   # ['b', 'a', 'c'] — insertion order preserved
 
# Reverse iteration (Python 3.8+)
for k in reversed(d):
    print(k, end=' ')   # c a b
print()
 
 
# ============================================================
# 7. DICTIONARY VIEWS
# ============================================================
# keys(), values(), items() return VIEW objects — not copies
# Views are LIVE: automatically reflect dict changes
 
d = {'a': 1, 'b': 2}
keys   = d.keys()
values = d.values()
items  = d.items()
 
d['c'] = 3
print(keys)    # dict_keys(['a', 'b', 'c'])         ← updated automatically
print(values)  # dict_values([1, 2, 3])              ← updated automatically
print(items)   # dict_items([('a',1),('b',2),('c',3)]) ← updated automatically
 
# dict_keys and dict_items support SET OPERATIONS
# dict_values does NOT — values may be non-unique or unhashable
d1 = {'a': 1, 'b': 2, 'c': 3}
d2 = {'b': 10, 'c': 20, 'd': 30}
 
print(d1.keys() & d2.keys())   # {'b', 'c'}          — shared keys
print(d1.keys() | d2.keys())   # {'a','b','c','d'}    — all keys
print(d1.keys() - d2.keys())   # {'a'}                — only in d1
 
# Practical: detect which config keys will be overridden
defaults  = {'timeout': 30, 'retries': 3, 'debug': False}
overrides = {'timeout': 60, 'verbose': True}
will_change = defaults.keys() & overrides.keys()
print(will_change)   # {'timeout'}
 
# ⚠️ Views are not subscriptable
# d.keys()[0]   ❌ TypeError
print(list(d.keys())[0])   # ✅ convert to list first
 
 
# ============================================================
# 8. SET THEORY AND COMMON USE
# ============================================================
# Set: unordered collection of unique, hashable objects
# Backed by a hash table — O(1) average membership, insert, delete
 
# Use case 1: O(1) membership testing
haystack = {'spam', 'eggs', 'bacon', 'toast'}
needles   = {'spam', 'toast', 'marmalade'}
 
found = needles & haystack          # intersection — in both
print(found)                        # {'spam', 'toast'}
print(len(needles & haystack))      # 2 — count matches without a loop
 
# Use case 2: deduplication (order NOT preserved)
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique = list(set(items))
print(sorted(unique))   # [1, 2, 3, 4, 5, 6, 9]
 
# Use case 3: fast difference / overlap between collections
required_fields  = {'name', 'email', 'role'}
submitted_fields = {'name', 'email', 'phone'}
 
missing = required_fields - submitted_fields   # {'role'}
extra   = submitted_fields - required_fields   # {'phone'}
print(f"Missing: {missing}, Extra: {extra}")
 
# ⚠️ Sets are unordered — no indexing
s = {3, 1, 2}
# s[0]   ❌ TypeError: 'set' object is not subscriptable
print(sorted(s))   # [1, 2, 3] — sort to get ordered output
 
# ⚠️ Elements must be hashable
# {[1, 2]}         ❌ TypeError: unhashable type: 'list'
# {{1: 2}}         ❌ TypeError: unhashable type: 'dict'
print({(1, 2), (3, 4)})   # ✅ tuples are hashable
 
 
# ============================================================
# 9. SET LITERALS AND FROZENSET
# ============================================================
s = {1, 2, 3}           # set literal — preferred over set([1,2,3])
print(type(s))          # <class 'set'>
 
# ⚠️ Critical trap — {} creates a DICT, not a set
empty_dict = {}
empty_set  = set()      # must use constructor for empty set
print(type(empty_dict)) # <class 'dict'>
print(type(empty_set))  # <class 'set'>
 
# Sets silently discard duplicates on creation
s = {1, 2, 2, 3, 3, 3}
print(s)   # {1, 2, 3}
 
# frozenset — immutable set, hashable itself
# Can be used as a dict key or as an element of another set
fs = frozenset({1, 2, 3})
# fs.add(4)   ❌ AttributeError — no mutation methods
 
d = {fs: 'value'}        # ✅ frozenset as dict key
nested = {{1, 2}}        # ❌ TypeError — regular set is not hashable
nested = {frozenset({1, 2}), frozenset({3, 4})}  # ✅
print(nested)
 
 
# ============================================================
# 10. SET COMPREHENSIONS
# ============================================================
# Syntax: {expression for var in iterable if condition}
# Produces a set — duplicates removed automatically
 
from unicodedata import name as uname
 
# All Unicode characters with 'SIGN' in their name, code points 32–255
signs = {chr(i) for i in range(32, 256) if 'SIGN' in uname(chr(i), '')}
print(signs)   # {'$', '©', '°', '×', '¥', ...} — unordered
 
# Unique word lengths in a list
words = ['apple', 'banana', 'fig', 'kiwi', 'cherry', 'pear']
unique_lengths = {len(w) for w in words}
print(sorted(unique_lengths))   # [3, 4, 5, 6]
 
# Extract unique domains from email list
emails = ['alice@gmail.com', 'bob@yahoo.com', 'carol@gmail.com', 'dave@outlook.com']
domains = {email.split('@')[1] for email in emails}
print(domains)   # {'gmail.com', 'yahoo.com', 'outlook.com'}
 
 
# ============================================================
# 11. SET OPERATIONS
# ============================================================
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}
 
# Operator form — both sides MUST be sets
print(a | b)    # {1,2,3,4,5,6,7}  — union
print(a & b)    # {3,4,5}           — intersection
print(a - b)    # {1,2}             — difference (in a, not in b)
print(a ^ b)    # {1,2,6,7}         — symmetric difference (in either, not both)
 
# Method form — accepts any ITERABLE, not just sets
print(a.union([3, 4, 8]))             # {1,2,3,4,5,8}
print(a.intersection((3, 4, 8)))      # {3,4}
print(a.difference(range(3, 6)))      # {1,2}
 
# In-place update versions
c = {1, 2, 3}
c |= {3, 4, 5}
print(c)   # {1, 2, 3, 4, 5}
 
# Subset / superset comparisons
print({1, 2} <= {1, 2, 3})    # True  — subset (≤, allows equal)
print({1, 2} <  {1, 2, 3})    # True  — proper subset (strictly smaller)
print({1, 2} <  {1, 2})       # False — equal sets are not proper subsets
print({1, 2, 3} >= {1, 2})    # True  — superset
print({1, 2} == {2, 1})        # True  — order irrelevant
 
# --- Practical: agent tool capability comparison ---
agent1_tools = {'search', 'summarize', 'translate', 'code'}
agent2_tools = {'search', 'summarize', 'image_gen', 'code'}
 
shared    = agent1_tools & agent2_tools   # {'search', 'summarize', 'code'}
unique_1  = agent1_tools - agent2_tools   # {'translate'}
unique_2  = agent2_tools - agent1_tools   # {'image_gen'}
all_tools = agent1_tools | agent2_tools   # full capability union
 
print(f"Shared: {shared}")
print(f"Only agent1: {unique_1}")
print(f"Only agent2: {unique_2}")
print(f"All: {all_tools}")
 