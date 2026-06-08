# Fluent Python Ch.3 — Dictionaries and Sets


## 1. Ways to Create a Dict

Five common patterns

```python
# 1. Literal — most common and readable
d = {'one': 1, 'two': 2, 'three': 3}

# 2. dict() with keyword args — keys must be valid Python identifiers
d = dict(one=1, two=2, three=3)
# dict(my-key=1)  ❌ SyntaxError — hyphens not allowed as identifiers

# 3. dict() from iterable of (key, value) pairs
d = dict([('one', 1), ('two', 2), ('three', 3)])

# 4. dict() + zip — pair two parallel lists
keys   = ['one', 'two', 'three']
values = [1, 2, 3]
d = dict(zip(keys, values)) # zip() a built-in Python function that combines multiple iterables element-by-element (index-based paring)

# 5. fromkeys — all keys share the same default value
d = dict.fromkeys(['spam', 'eggs', 'bacon'], 0) 
# dict.fromkeys(keys, value) - creates a new dictionary using the items in keys as the keys, and assigns the same value to each key, value can be optional (then default None)
# {'spam': 0, 'eggs': 0, 'bacon': 0}
```

###  fromkeys Mutable Default Trap
```python
# All keys share the SAME list object — mutating one mutates all
d = dict.fromkeys(['a', 'b', 'c'], [])
d['a'].append(1)
print(d)   # {'a': [1], 'b': [1], 'c': [1]}  ← not what you wanted

# Fix: use a dict comprehension — each key gets its OWN object
d = {k: [] for k in ['a', 'b', 'c']}
d['a'].append(1)
print(d)   # {'a': [1], 'b': [], 'c': []}  ✅
```


## 2. Dict Comprehensions

```python
# Syntax: {key_expr: value_expr for var in iterable if condition}
# Builds a new dict from any iterable of key:value pairs

dial_codes = [(880, 'Bangladesh'), (55, 'Brazil'), (86, 'China'), (91, 'India')]

# Basic — swap key and value
country_to_code = {country: code for code, country in dial_codes}
# {'Bangladesh': 880, 'Brazil': 55, 'China': 86, 'India': 91}

# With filter condition
large_codes = {code: country for code, country in dial_codes if code > 80}
# {880: 'Bangladesh', 86: 'China', 91: 'India'}
```

### C++ Parallel
Dict comprehensions are like building a `std::unordered_map` from a range
in one expression — no separate insert loop needed.


## 3. Merging Mappings — `|` and `|=`

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

# | creates a NEW merged dict — d1 and d2 unchanged
merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}
print(d1)      # {'a': 1, 'b': 2}  — untouched
# Rightmost dict WINS on key conflicts — d2's 'b': 3 overwrites d1's 'b': 2

# |= updates IN-PLACE
d1 |= d2
print(d1)      # {'a': 1, 'b': 3, 'c': 4}
```

###  Common Trap
```python
# update() also merges in-place but returns None — never assign it
result = d1.update(d2)
print(result)   # None  ← you lost the dict reference

# Before Python 3.9, the standard merge pattern was:
merged = {**d1, **d2}   # still valid, still common in older codebases
```


## 4. Pattern Matching with Mappings

```python
# match/case on dicts is PARTIAL — extra keys in the subject are ignored
# Only the keys listed in the pattern need to be present

def get_creators(record: dict) -> list:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            # [*names] — value must be a list; captures ALL elements into names
            return names

        case {'type': 'book', 'api': 1, 'author': str(name)}:
            # str(name) — type-checks AND binds: only matches if value is a str
            return [name]

        case {'type': 'book', 'api': 1, 'author': name}:
            # bare name — matches ANY value for 'author', no type check
            return [name]

        case {'type': 'book'}:
            raise ValueError(f"Invalid book record: {record}")

        case _:
            raise ValueError(f"Unknown record: {record}")
```

### Pattern Syntax Reference
| Pattern | Matches | Binds |
|---|---|---|
| `'author': name` | any value | value as-is |
| `'author': str(name)` | only `str` values | the string |
| `'authors': [*names]` | only lists | all elements as a list |
| `'authors': [first, *rest]` | list with ≥1 element | first element + remainder |
| `'api': 2` | exact literal `2` only | nothing (no binding) |

###  Common Trap
```python
# Dict patterns do NOT require an exact match — extra keys are fine
record = {'type': 'book', 'api': 2, 'authors': ['Alice'], 'isbn': '123'}
# Still matches case 1 — 'isbn' is silently ignored
# This is intentional: dicts often carry extra metadata you don't care about
```


## 5. Standard API — Read, Write, Default Handling

```python
d = {'a': 1, 'b': 2, 'c': 3}

# --- Read ---
d['a']           # 1  — KeyError if missing
d.get('z')       # None — safe, no exception
d.get('z', 0)    # 0   — with explicit default

# Membership — O(1), same as set
'a' in d         # True
'z' not in d     # True

# --- Write ---
d['z'] = 99      # insert or update
del d['a']       # KeyError if key absent

# --- Default handling patterns ---

# setdefault: insert key with default ONLY if absent, then return value
# Avoids the double-lookup anti-pattern
d.setdefault('hits', []).append('page1') # do the two lookups at once

# Anti-pattern — two lookups: - traditonal way
if 'hits' not in d:
    d['hits'] = []
d['hits'].append('page1')

# defaultdict: auto-creates missing keys using a factory function
from collections import defaultdict

# type annotation, variable_name : type = value
# defaultdict(list) -> creates the defaultdict object.
index: defaultdict[str, list] = defaultdict(list)  # list -> factory function
for word in ['hello', 'world', 'hello']:
    index[word].append(1)      # no KeyError — [] created automatically
print(dict(index))   # {'hello': [1, 1], 'world': [1]}

# defaultdict(factory)
# "When a key is missing, create a default value by calling factory()."

# traditional way
index = {}
for word in ["hello", "world", "hello"]:
    if word not in index:
        index[word] = []

    index[word].append(1)
```

###  defaultdict Trap
```python
# The factory must be a CALLABLE with no arguments
defaultdict(list)     # ✅ — list() called on each missing key, creates new []
defaultdict(list())   # ❌ — passes [] as the default_factory, not callable
                      #       all missing keys share the SAME list object
```


## 6. Common Mapping Methods

```python
d = {'a': 1, 'b': 2, 'c': 3}

d.pop('a')            # remove and return value — KeyError if absent
d.pop('z', None)      # safe pop with default
d.popitem()           # remove and return LAST inserted (key, value) — LIFO
d.clear()             # remove all items
d2 = d.copy()         # shallow copy — nested objects still shared

# Iteration — insertion order guaranteed since Python 3.7
for k, v in d.items():
    print(k, v)

# Reverse iteration (Python 3.8+)
for k in reversed(d):
    print(k)
```

###  popitem() is LIFO, not random
```python
d = {'a': 1, 'b': 2, 'c': 3}
print(d.popitem())   # ('c', 3) — last inserted, always
# Use pop(key) if you need a specific key removed
```

### Insertion Order Matters in Practice
```python
# Pipeline steps, config layers, LLM tool registries — order is preserved
pipeline = {}
pipeline['validate']  = validate_fn
pipeline['transform'] = transform_fn
pipeline['load']      = load_fn
# Iterating pipeline.items() always yields steps in insertion order
```


## 7. Dictionary Views

```python
# keys(), values(), items() return VIEW objects — not copies
# Views are LIVE: they reflect dict changes automatically, no re-call needed

d = {'a': 1, 'b': 2}
keys = d.keys()
d['c'] = 3
print(keys)   # dict_keys(['a', 'b', 'c'])  ← updated automatically

# dict_keys and dict_items support SET OPERATIONS
# dict_values does NOT — values may be non-unique or unhashable
d1 = {'a': 1, 'b': 2}
d2 = {'b': 3, 'c': 4}

d1.keys() & d2.keys()   # {'b'}            — shared keys (intersection)
d1.keys() | d2.keys()   # {'a', 'b', 'c'}  — all keys (union)
d1.keys() - d2.keys()   # {'a'}            — only in d1 (difference)

# Practical: find keys that will be overridden in a config merge
defaults  = {'timeout': 30, 'retries': 3, 'debug': False}
overrides = {'timeout': 60, 'verbose': True}
changed = defaults.keys() & overrides.keys()
print(changed)   # {'timeout'}
```

###  Views Are Not Subscriptable
```python
d.keys()[0]          # ❌ TypeError: 'dict_keys' object is not subscriptable
list(d.keys())[0]    # ✅ convert to list first if you need indexing
```


## 8. Set Theory and Common Use

A set is an **unordered collection of unique, hashable objects**.
Backed by a hash table — same underlying structure as dict keys.

```python
# Primary use 1: O(1) membership testing
haystack = {'spam', 'eggs', 'bacon'}
'spam' in haystack              # O(1) — hash lookup
'spam' in ['spam', 'eggs']      # O(n) — linear scan

# Primary use 2: deduplication
words = ['apple', 'banana', 'apple', 'cherry', 'banana']
unique = list(set(words))   # order NOT guaranteed after dedup

# Primary use 3: set operations on collections
post1_tags = {'python', 'backend', 'api'}
post2_tags = {'python', 'ml', 'api'}
common   = post1_tags & post2_tags   # {'python', 'api'}
only_p1  = post1_tags - post2_tags   # {'backend'}
```

### C++ Parallel
`set` ≈ `std::unordered_set` — O(1) average lookup via hashing.
`frozenset` ≈ `const std::unordered_set` — immutable, hashable itself.

###  Common Traps
```python
# Sets are unordered — no indexing
s = {1, 2, 3}
s[0]        # ❌ TypeError: 'set' object is not subscriptable

# Elements must be hashable — no mutable containers inside a set
{[1, 2]}    # ❌ TypeError: unhashable type: 'list'
{(1, 2)}    # ✅ tuples are hashable (if all elements are hashable)

# frozenset is hashable — can be a dict key or nested in another set
fs = frozenset({1, 2})
d = {fs: 'value'}   # ✅
```


## 9. Set Literals

```python
s = {1, 2, 3}           # set literal — preferred, faster than set()
s = {'a', 'b', 'c'}

# ⚠️ Critical trap — empty set has NO literal syntax
{}          # dict, NOT a set
set()       # ✅ empty set — must use the constructor

# frozenset — also has no literal syntax
fs = frozenset({1, 2, 3})
fs.add(4)   # ❌ AttributeError — frozenset is immutable

# Sets silently discard duplicates
s = {1, 2, 2, 3, 3, 3}
print(s)    # {1, 2, 3}

# Mixed hashable types are fine
s = {1, 'two', (3, 4), frozenset([5, 6])}   # ✅
```


## 10. Set Comprehensions

```python
# Syntax: {expression for var in iterable if condition}
# Same as listcomp but produces a set — duplicates removed automatically

from unicodedata import name

# All Unicode characters with 'SIGN' in their name, code points 32–255
signs = {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
# {'$', '©', '°', '×', '¥', ...}  — unordered, unique

# Unique word lengths in a corpus
words = ['apple', 'banana', 'fig', 'kiwi', 'cherry']
unique_lengths = {len(w) for w in words}
print(unique_lengths)   # {3, 4, 5, 6}
```


## 11. Set Operations

```python
a = {1, 2, 3, 4, 5}
b = {3, 4, 5, 6, 7}

# Operator form — both sides must be sets
a | b    # {1,2,3,4,5,6,7}  — union
a & b    # {3,4,5}           — intersection
a - b    # {1,2}             — difference (in a, not in b)
a ^ b    # {1,2,6,7}         — symmetric difference (in either, not both)

# Method form — accepts any iterable, not just sets
a.union([3, 4, 8])
a.intersection((3, 4, 8))

# In-place update
a |= b       # union, updates a in-place
a &= b       # intersection, updates a in-place
a -= b       # difference, updates a in-place
a ^= b       # symmetric difference, updates a in-place

# Subset / superset comparisons
{1, 2} <= {1, 2, 3}    # True — subset
{1, 2} <  {1, 2, 3}    # True — proper subset (strictly smaller, not equal)
{1, 2, 3} >= {1, 2}    # True — superset
{1, 2} == {2, 1}        # True — order irrelevant in equality
```

### Practical: Agent / RAG Use Case
```python
# Compare tool capabilities across two agent configs
agent1_tools = {'search', 'summarize', 'translate', 'code'}
agent2_tools = {'search', 'summarize', 'image_gen', 'code'}

shared    = agent1_tools & agent2_tools   # {'search', 'summarize', 'code'}
unique_1  = agent1_tools - agent2_tools   # {'translate'}
unique_2  = agent2_tools - agent1_tools   # {'image_gen'}
all_tools = agent1_tools | agent2_tools   # full capability union
```


## 12. Counter
# Counter is a class from the built-in module collections used to count how many times each element appears in a collection (like a list, string, or tuple)

```python
# create a Counter
from collections import Counter

# 1. From an iterable — counts occurrences automatically
ct = Counter('abracadabra')
print(ct)   # Counter({'a': 5, 'b': 2, 'r': 2, 'c': 1, 'd': 1})

# 2. From a sequence of words
word_count = Counter(['spam', 'eggs', 'spam', 'bacon', 'spam'])
print(word_count)   # Counter({'spam': 3, 'eggs': 1, 'bacon': 1})

# 3. From keyword args
ct = Counter(a=3, b=2, c=1)


# important methods
ct = Counter('abracadabra')

# most_common(n) — returns top n (key, count) pairs, sorted by count
ct.most_common(3)   # [('a', 5), ('b', 2), ('r', 2)]
ct.most_common(1)   # [('a', 5)]

# Missing keys return 0 — no KeyError (unlike plain dict)
ct['z']   # 0

# update() — ADDS counts, does not replace
ct.update('aaa')
ct['a']   # 8  (was 5, added 3)

# subtract() — subtracts counts, can go negative
ct.subtract('aab')
ct['a']   # 6, ct['b']  # 1


# arithmetic on Counters
c1 = Counter(a=3, b=2)
c2 = Counter(a=1, b=4, c=1)

c1 + c2   # Counter({'b': 6, 'a': 4, 'c': 1}) — add counts
c1 - c2   # Counter({'a': 2})                  — subtract, drop ≤ 0
c1 & c2   # Counter({'a': 1, 'b': 2})          — min of each count
c1 | c2   # Counter({'b': 4, 'a': 3, 'c': 1}) — max of each count


# key traps
# update() adds, not replaces — opposite of dict.update()
ct = Counter(a=3)
ct.update({'a': 2})
print(ct['a'])   # 5, not 2

# - operator drops zero and negative counts
# subtract() keeps them; - does not
c = Counter(a=2)
c.subtract({'a': 5})
print(c['a'])    # -3  ← subtract() keeps negatives
c2 = Counter(a=2) - Counter(a=5)
print(c2)        # Counter()  ← - drops non-positive results

# Counter is a dict — all dict methods work
dict(ct)         # convert back to plain dict
list(ct.elements())  # expand back to list with repetitions: ['a','a','a',...]
```



## Quick Mental Model

| Python Type | Underlying Structure | Avg Lookup | C++ Analogy |
|---|---|---|---|
| `dict` | Hash table (key → value) | O(1) | `std::unordered_map` |
| `set` | Hash table (key only) | O(1) | `std::unordered_set` |
| `frozenset` | Immutable hash table | O(1) | `const std::unordered_set` |
| `defaultdict` | dict + missing-key factory | O(1) | `map` with `operator[]` auto-insert |


## Quick Reference Card

| Concept | Key Point | Trap |
|---|---|---|
| `fromkeys` | All keys share one default value | Mutable default is shared — use comprehension instead |
| Dict comprehension | `{k: v for ...}` — each value is independent | — |
| `\|` vs `\|=` | `\|` → new dict; `\|=` → in-place | `update()` returns `None` — never assign it |
| `{**d1, **d2}` | Pre-3.9 merge pattern — still valid | Rightmost key wins on conflict |
| Dict pattern matching | Partial match — extra keys ignored | `str(name)` type-checks; bare `name` accepts anything |
| `setdefault` | Insert-if-absent + return in one lookup | Double lookup anti-pattern: `in` check + assign separately |
| `defaultdict` | Auto-creates missing keys via factory | Pass callable: `defaultdict(list)` not `defaultdict([])` |
| `popitem()` | Removes LAST inserted pair — LIFO | Not random — use `pop(key)` for a specific key |
| Dict views | Live window into dict — auto-updates | Not subscriptable; `dict_values` has no set operations |
| Empty set | Must use `set()` — no literal | `{}` creates an empty **dict** |
| Set elements | Must be hashable | Lists inside sets → `TypeError` |
| `frozenset` | Immutable, hashable — usable as dict key | No literal syntax — use `frozenset({...})` |
| Operator vs method | `&` requires sets on both sides | `.intersection(iterable)` accepts any iterable |