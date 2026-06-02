---

# Fluent Python Ch.6 — Object References, Mutability, and Recycling
# Key notes for C++ → Python transition

---

## 1. Variables are labels, not boxes

Python:
  - A variable is a label (reference/pointer) attached to an object
  - The object exists independently; multiple labels can point to it
  - Assignment `=` never copies data — it just binds a name to an object

C++ comparison:
  int x = 5;      // x IS the box containing 5, stored on stack
  int y = x;      // y is a full independent copy

  x = [1,2,3]     # Python: x is a label pointing to a list object in heap
  y = x           # y is another label to the SAME object — no copy made


## 2. == vs is

  ==   compares VALUE (calls __eq__)        — like comparing *p1 == *p2 in C++
  is   compares IDENTITY (memory address)   — like comparing p1 == p2 (raw pointers)

  x = [1, 2, 3]
  y = [1, 2, 3]
  x == y   # True  — same value
  x is y   # False — different objects

  TRAP: Never use `is` to compare values. Only use `is` for:
    - checking `if x is None`
    - checking `if x is True / False`

  C++ has no direct equivalent of `is` for value types.
  Closest analogy: comparing two pointers vs dereferencing them.


## 3. Aliasing

  a = [1, 2, 3]
  b = a           # b is an alias — same object
  b.append(4)
  print(a)        # [1, 2, 3, 4] — a is affected

  C++ comparison:
    std::vector<int>& b = a;  // explicit reference syntax required
    // Python does this silently on every assignment


## 4. Tuple's relative immutability — TRAP

  - Tuple cannot have items added/removed (the container is immutable)
  - BUT if a tuple contains a mutable object, that object CAN be mutated

  t = ([1, 2], 3)
  t[0].append(99)
  print(t)        # ([1, 2, 99], 3) — tuple "changed"!

  The tuple's references are fixed — but the objects those references
  point to can still be mutated if they are mutable.

  This is why tuples are not always safe as dict keys —
  only tuples containing purely immutable objects are truly hashable.


## 5. Copies are shallow by default — TRAP

  list(l1) / l1[:] / copy.copy(l1)  all produce SHALLOW copies:
    - new outer container is created
    - but inner elements are still shared references

  l1 = [[1, 2], [3, 4]]
  l2 = l1[:]
  l2[0].append(99)
  print(l1[0])    # [1, 2, 99] — inner list is shared!

  C++ comparison:
    Shallow ~ copying a struct that holds a raw pointer
              (pointer value copied, not the thing it points to)
    Deep    ~ copying a struct and allocating new memory for pointee

  Use copy.deepcopy() when nested mutable objects must be independent.
  Deepcopy is slower — only use when actually needed.


## 6. Call by sharing (function parameters)

  - Parameters are aliases of the actual arguments — no copy is made
  - Function CAN mutate a mutable argument (caller sees the change)
  - Function CANNOT rebind the caller's variable

  def append_one(lst):
      lst.append(1)       # mutates — caller sees it

  def replace(lst):
      lst = [99]          # rebinds local name only — caller unaffected

  For immutable types (int, str, tuple):
    += always creates a new object and rebinds locally — caller never affected

  C++ comparison:
    C++ requires explicit & to pass by reference
    Python passes everything by reference silently — no opt-in needed


## 7. Mutable default argument trap — COMMON BUG

  def __init__(self, passengers=[]):   # BUG

  The [] is created ONCE at function definition time, stored permanently
  on the function object in __defaults__. Every call that omits the
  argument shares that same list.

  C++ difference:
    C++ default args are substituted fresh at each call site by the compiler
    Python default args are real objects stored on the function object

  FIX — always use None as default for mutable types:
    def __init__(self, passengers=None):
        self.passengers = [] if passengers is None else list(passengers)


## 8. Defensive copy for mutable parameters

  self.passengers = list(passengers)   # shallow copy — new container

  Why this is enough for a flat list of strings:
    - .append() / .remove() modify the container, not the elements
    - strings are immutable so sharing element references is safe

  When it's NOT enough:
    - If elements are mutable objects (nested lists, dicts)
    - Then use copy.deepcopy()


## 9. del and garbage collection

  del x   — deletes the LABEL (reference), not the object
            object is only garbage collected when reference count hits 0

  C++ comparison:
    delete ptr;   — explicitly destroys the object and frees memory
    Python:       — memory managed automatically via reference counting
                    (+ cyclic garbage collector for reference cycles)

  CPython uses reference counting.
  Other implementations (PyPy, Jython) may use different GC strategies.


## 10. Immutable types optimization

  For tuple and str, Python skips making a copy and returns same object:
    t = (1, 2, 3)
    t2 = t[:]
    t is t2   # True — same object, no copy made

  Safe because immutability guarantees they can never diverge.
  Lists must make real copies since mutation would create aliasing bugs.

  CPython also interns small integers (-5 to 256) and some strings —
  same optimization, same reason.


## 11. += and *= on immutable vs mutable types

  Immutable (int, str, tuple):
    x = 1
    x += 1      # new int object created, x rebound to it

  Mutable (list):
    a = [1, 2]
    a += [3]    # calls __iadd__, mutates in place, no rebinding

  TRAP — tuple containing a list:
    t = ([1, 2], 3)
    t[0] += [4]     # raises TypeError BUT also mutates t[0] first!
                    # t is now ([1, 2, 4], 3) despite the exception
    Lesson: never put mutable objects inside tuples.

---

## Quick reference — C++ vs Python memory model

| Concept              | C++                              | Python                            |
|----------------------|----------------------------------|-----------------------------------|
| Variable             | named box holding value          | label pointing to object          |
| Assignment           | copies value                     | binds label to object             |
| Pass to function     | copy by default, & for reference | always reference (call by sharing)|
| Default arg values   | substituted fresh each call      | one object stored on function     |
| Memory management    | manual (delete) or RAII          | automatic reference counting      |
| Copy                 | deep by default                  | shallow by default                |
```

---


See: `w01-python-fast-track/d1_memory_model.py`
