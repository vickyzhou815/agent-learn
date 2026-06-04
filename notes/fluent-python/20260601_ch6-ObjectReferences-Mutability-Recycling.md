
# Fluent Python Ch.6 — Object References, Mutability, and Recycling
### Key notes for C++ → Python transition


## 1. Variables are labels, not boxes

Python variables are labels (references/pointers) attached to objects. The object exists
independently; multiple labels can point to it. Assignment `=` never copies data — it just
binds a name to an object.

**C++ comparison:**

```cpp
int x = 5;   // x IS the box containing 5, stored on stack
int y = x;   // y is a full independent copy
```

```python
x = [1, 2, 3]  # x is a label pointing to a list object in heap
y = x           # y is another label to the SAME object — no copy made
```


## 2. `==` vs `is`

| Operator | Compares | C++ equivalent |
|----------|----------|----------------|
| `==` | Value (calls `__eq__`) | `*p1 == *p2` (dereference) |
| `is` | Identity (memory address) | `p1 == p2` (raw pointer) |

```python
x = [1, 2, 3]
y = [1, 2, 3]
x == y   # True  — same value
x is y   # False — different objects
```

> **TRAP:** Never use `is` to compare values.
> Only use `is` for: `if x is None` / `if x is True` / `if x is False`


## 3. Aliasing

```python
a = [1, 2, 3]
b = a           # b is an alias — same object
b.append(4)
print(a)        # [1, 2, 3, 4] — a is affected
print(a is b)   # True
```

**C++ comparison:**

```cpp
std::vector<int>& b = a;  // explicit reference syntax required
// Python does this silently on every assignment — no & needed
```


## 4. Tuple's relative immutability — TRAP

Tuple cannot have items added/removed (the container is immutable), BUT if a tuple
contains a mutable object, that object CAN still be mutated.

```python
t = ([1, 2], 3)
t[0].append(99)
print(t)        # ([1, 2, 99], 3) — tuple "changed"!
```

The tuple's references are fixed — but the objects those references point to can still
be mutated if they are mutable.

> **Note:** This is why tuples are not always safe as dict keys — only tuples containing
> purely immutable objects are truly hashable.


## 5. Copies are shallow by default — TRAP

`list(l1)` / `l1[:]` / `copy.copy(l1)` all produce **shallow copies**:
- New outer container is created
- But inner elements are still shared references

```python
l1 = [[1, 2], [3, 4]]
l2 = l1[:]
l2[0].append(99)
print(l1[0])    # [1, 2, 99] — inner list is shared!
```

**C++ comparison:**

```
Shallow ~ copying a struct that holds a raw pointer
          (pointer value copied, not the thing it points to)
Deep    ~ copying a struct and allocating new memory for pointee
```

```python
import copy
deep = copy.deepcopy(l1)   # fully independent at all levels
```

> Use `copy.deepcopy()` when nested mutable objects must be independent.
> Deepcopy is slower — only use when actually needed.


## 6. Call by sharing (function parameters)

Parameters are aliases of the actual arguments — no copy is made on function call.

| Operation inside function | Caller sees change? |
|---------------------------|---------------------|
| Mutate the object (`lst.append(1)`) | ✅ Yes |
| Rebind local name (`lst = [99]`) | ❌ No |

```python
def append_one(lst):
    lst.append(1)       # mutates — caller sees it

def replace(lst):
    lst = [99]          # rebinds local name only — caller unaffected
```

For immutable types (int, str, tuple): `+=` always creates a new object and rebinds
locally — caller is never affected.

**C++ comparison:**

```
C++ requires explicit & to pass by reference
Python passes everything by reference silently — no opt-in needed
```


## 7. Mutable default argument trap — COMMON BUG

```python
def __init__(self, passengers=[]):   # BUG
```

The `[]` is created **once at function definition time**, stored permanently on the
function object in `__defaults__`. Every call that omits the argument shares that
same list.

```python
# You can actually inspect it:
print(HauntedBus.__init__.__defaults__)  # (['Alice'],) — accumulates over time!
```

**C++ difference:**

```
C++    — default args substituted fresh at each call site by the compiler
Python — default args are real objects stored on the function object
```

**FIX — always use `None` as default for mutable types:**

```python
def __init__(self, passengers=None):
    self.passengers = [] if passengers is None else list(passengers)
```


## 8. Defensive copy for mutable parameters

```python
self.passengers = list(passengers)   # shallow copy — new container
```

Why a shallow copy is enough for a flat list of strings:
- `.append()` / `.remove()` modify the **container**, not the elements
- Strings are immutable so sharing element references is safe

When it is **NOT** enough:
- If elements are mutable objects (nested lists, dicts)
- In that case use `copy.deepcopy()`


## 9. `del` and garbage collection

```python
del x   # deletes the LABEL (reference), not the object
        # object only garbage collected when reference count hits 0
```

**C++ comparison:**

```cpp
delete ptr;   // explicitly destroys the object and frees memory
```

```
Python — memory managed automatically via reference counting
         (+ cyclic garbage collector handles reference cycles)

Note: CPython uses reference counting.
      Other implementations (PyPy, Jython) may use different GC strategies.
```


## 10. Immutable types optimization

For `tuple` and `str`, Python skips making a copy and returns the same object:

```python
t = (1, 2, 3)
t2 = t[:]
print(t is t2)   # True — same object, no copy made

s = "hello"
s2 = s[:]
print(s is s2)   # True
```

Safe because immutability guarantees they can never diverge. Lists must make real
copies since mutation would create aliasing bugs.

> CPython also interns small integers (-5 to 256) and some strings — same
> optimization, same reason.


## 11. `+=` and `*=` on immutable vs mutable types

**Immutable (int, str, tuple) — new object created, name rebound:**

```python
x = 1
x += 1      # new int object created, x rebound to it
```

**Mutable (list) — mutated in place:**

```python
a = [1, 2]
a += [3]    # calls __iadd__, mutates in place, no rebinding
```

**TRAP — tuple containing a list:**

```python
t = ([1, 2], 3)
t[0] += [4]     # raises TypeError BUT also mutates t[0] first!
                # t is now ([1, 2, 4], 3) despite the exception
```

> **Lesson:** Never put mutable objects inside tuples.


## Quick reference — C++ vs Python memory model

| Concept | C++ | Python |
|---|---|---|
| Variable | Named box holding value | Label pointing to object |
| Assignment | Copies value | Binds label to object |
| Pass to function | Copy by default, `&` for reference | Always reference (call by sharing) |
| Default arg values | Substituted fresh each call | One object stored on function |
| Memory management | Manual (`delete`) or RAII | Automatic reference counting |
| Copy | Deep by default | Shallow by default |