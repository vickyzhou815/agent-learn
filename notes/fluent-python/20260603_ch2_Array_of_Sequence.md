
# Fluent Python Ch.2 — An Array of Sequences


## 1. Sequence Taxonomy

### By Storage Model
| Category | Examples | Stores |
|---|---|---|
| **Container sequence** | `list`, `tuple`, `deque` | References (pointers) to objects of any type |
| **Flat sequence** | `str`, `bytes`, `array.array` | Values directly in its own memory (C-style) |

### By Mutability
| Category | Examples |
|---|---|
| **Mutable** | `list`, `bytearray`, `array.array`, `deque` |
| **Immutable** | `tuple`, `str`, `bytes` |

**C++ mental model**: Container sequences are like `std::vector<void*>` — they hold pointers, not values. Flat sequences are like true C arrays — values are inline in memory.


## 2. List Comprehensions (Listcomps)

```python
codes = [ord(s) for s in symbols if ord(s) > 127]  # ord() converts a character to its Unicode code point
```

- Syntax: `[expression for var in iterable if condition]`
- The loop variable (`s`, `c`, etc.) is **local** to the comprehension — gone after it finishes
- Preferred over `map`/`filter` in Python for readability

### Walrus Operator `:=` — Assign AND Return
```python
codes = [last := ord(c) for c in symbols]
# last is accessible AFTER the comprehension (leaks to enclosing scope)
# c is NOT accessible after (normal loop variable, local only)
```

### ⚠️ Common Trap
```python
x = 10
result = [x for x in range(3)]  # loop var x is local
print(x)  # still 10 — outer x is NOT clobbered (Python 3)
```


## 3. Listcomps vs `map`/`filter`

```python
# Listcomp — readable, left-to-right
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]

# map/filter — inside-out, needs lambda and list() wrap
# map() applies the function to every element in the iterable
# filter(function, iterable) - Keep only elements for which the function returns True
beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
```

- **Performance**: roughly equal
- **Prefer listcomps** — no `lambda`, no `list()` wrap, reads naturally
- `map`/`filter` return **lazy iterators** — need `list()` to materialize


## 4. Generator Expressions (Genexps)

Same syntax as listcomps but with **parentheses** instead of brackets.

```python
# Listcomp — builds entire list in memory first
[ord(s) for s in symbols]

# Genexp — yields one item at a time, memory efficient
(ord(s) for s in symbols)
```

```python
# Use genexp to initialize other sequences
import array
arr = array.array('I', (ord(s) for s in symbols))  # no intermediate list built
```

**When to use**: When you only need to iterate once and don't need the full list in memory. Essential for large datasets.


## 5. Tuples

### As Records (semantic use)
```python
city, year, pop = ('Tokyo', 2003, 32_450)  # unpacking
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567')]
```
Position carries meaning. Treat like a lightweight struct.

### As Immutable Lists (structural use)
- Slightly less memory than `list`
- Communicates intent: "this will not change"
- Can be used as `dict` keys (hashable, if all elements are hashable)

### ⚠️ Critical Trap — Tuple "Immutability"
```python
t = (1, 2, [3, 4])
t[2].append(5)
print(t)  # (1, 2, [3, 4, 5]) — tuple "changed"!
```
**Immutability applies to the references, not the objects they point to.**
The tuple cannot have its references deleted or replaced, but if a reference points to a mutable object, that object can still be mutated.

```python
t[2] = [99]   # ❌ TypeError — can't replace the reference
t[2].append(5)  # ✅ mutates the list object the reference points to
```


## 6. Unpacking Iterables

```python
# Basic unpacking
a, b, c = (1, 2, 3)

# Swap without temp variable
a, b = b, a

# Star unpacking — grab the rest
first, *rest = [1, 2, 3, 4]     # first=1, rest=[2,3,4]
*head, last = [1, 2, 3, 4]      # head=[1,2,3], last=4
first, *mid, last = [1,2,3,4,5] # first=1, mid=[2,3,4], last=5

# Nested unpacking
(a, b), c = (1, 2), 3
```

### ⚠️ Common Trap
```python
a, b = 1, 2, 3  # ❌ ValueError: too many values to unpack
```


## 7. Slicing

```python
seq[start:stop:step]
```

- **Stop is exclusive** — `seq[1:4]` gives indices 1, 2, 3
- Negative step reverses: `seq[::-1]` reverses the sequence
- `seq[::2]` every other element

```python
s = 'bicycle'
s[::3]   # 'bye'
s[::-1]  # 'elcycib'
s[-3:]   # 'cle' (last 3)
```

### Named Slices (interview-worthy pattern)
```python
PRICE = slice(40, 52)
line[PRICE]  # much more readable than line[40:52] scattered in code
```

### Slice Assignment (mutable sequences only)
```python
l = list(range(10))
l[2:5] = [20, 30]    # replace a section
del l[5:7]           # delete a section
```


## 8. `list.sort` vs `sorted`

| | `list.sort()` | `sorted()` |
|---|---|---|
| Modifies original | ✅ in-place | ❌ returns new list |
| Works on | lists only | any iterable |
| Return value | `None` | new sorted list |

```python
fruits = ['grape', 'raspberry', 'apple']
sorted(fruits)          # new list, fruits unchanged
sorted(fruits, reverse=True)
sorted(fruits, key=len) # sort by length

fruits.sort()           # in-place, returns None
```

### ⚠️ Common Trap
```python
result = my_list.sort()  # result is None!
# Use sorted() if you need the return value
```

**Key insight**: `list.sort()` returning `None` is a Python convention — signals in-place mutation (contrast with methods that return `self` for chaining).


## 9. `array.array` vs `list`

| | `list` | `array.array` |
|---|---|---|
| Storage | Array of pointers to objects | Raw C values, inline |
| Type restriction | Any mix of types | Single type only (e.g. `'d'` for double) |
| Memory | High (each element is a full Python object) | Low (just the raw values) |
| Speed for numerics | Slower | Faster |

```python
import array
floats = array.array('d', (random() for _ in range(10**7)))
```

Use `array.array` when storing millions of numbers. Use `numpy` for numerical computation.


## Quick Reference

| Concept | Key Point | Trap |
|---|---|---|
| Container vs Flat | list stores pointers; array stores values | Don't assume list is compact |
| Listcomp scope | loop var is local | `:=` leaks to outer scope |
| Tuple immutability | references are fixed, not the objects | Mutable contents can still change |
| Slicing | stop is **exclusive** | `seq[1:4]` → indices 1,2,3 only |
| `list.sort()` | in-place, returns `None` | Never assign the return value |
| Unpacking | star collects remainder into a list | Count must match without star |