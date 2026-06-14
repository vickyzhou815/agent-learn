Ref: https://realpython.com/python-data-classes/

## Python Dataclasses

### The Core Idea

`@dataclass` automatically generates `__init__()`, `__repr__()`, and `__eq__()` — eliminating the boilerplate you'd otherwise write by hand. Think of it like C++ structs with auto-generated constructors and comparison operators, but wired up via a decorator.

```python
@dataclass
class Position:
    name: str
    lon: float = 0.0
    lat: float = 0.0
```

That's it. You get a constructor, a nice `repr`, and value-based equality for free.



### Alternatives Compared

`namedtuple` gives similar output but compares equal to plain tuples and other namedtuples with the same field values — a type-safety footgun. `attrs` (third-party) is more powerful but adds a dependency. Dataclasses are the stdlib sweet spot.



### Key Features

**Default values** work inline for scalars. For mutable defaults (lists, dicts), you *must* use `field(default_factory=...)`:

```python
cards: List[PlayingCard] = field(default_factory=make_french_deck)
```

Using a mutable object directly as a default would cause all instances to share the same list — the classic Python mutable default argument trap (analogous to a C++ static local variable shared across all instances).

**Type hints are syntactically required** to declare fields, but they are not enforced at runtime. Use `typing.Any` if you genuinely don't want to constrain a type.

**`field()` parameters of note:**

| Parameter | Purpose |
|---|---|
| `default` / `default_factory` | Scalar vs. mutable defaults |
| `init=False` | Exclude from constructor (computed fields) |
| `repr=False` | Hide from `__repr__` |
| `compare=False` | Exclude from `__eq__` / ordering |
| `metadata` | Attach arbitrary info (e.g. units) |

**Ordering** is opt-in via `@dataclass(order=True)`. Comparison is done field-by-field as if the fields were a tuple, so field declaration order matters. For custom ordering, compute a `sort_index` field in `__post_init__()` and mark it `init=False, repr=False`.

**Immutability** via `frozen=True` raises `FrozenInstanceError` on assignment — like a `const` struct. However, nested mutable fields (e.g. a `list`) can still be mutated in-place — shallow freeze only.

**Inheritance** works normally, but a non-default field in a subclass cannot follow a defaulted field from a base class (same rule as Python function signatures — no positional after keyword defaults).

**Slots optimization**: You can add `__slots__` manually to a dataclass. Slot-based classes use roughly 44% less memory and attribute access is ~35% faster — relevant if you're creating many instances.



### Quick Mental Model (C++ analogy)

| Python dataclass feature | C++ equivalent feel |
|---|---|
| `@dataclass` | `struct` + auto-generated ctor/`operator==` |
| `frozen=True` | `const` instance (shallow) |
| `field(init=False)` | Member computed in ctor body, not in initializer list |
| `__post_init__` | Constructor body after member initialization |
| `__slots__` | Removing `__dict__` → tighter memory layout |

