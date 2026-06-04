
# Fluent Python Ch.8 — Type Hints in Functions


## 1. Type Hints

Declare the expected types of variables, function parameters, and return values.

> Not enforced at runtime — only useful with tools like `mypy`, `pyright`, or IDE type checkers.

```python
def add(a: int, b: int) -> int:
    return a + b

add("hello", "world")  # Runs fine at runtime
                        # mypy would flag this as an error
```


## 2. Gradual Typing

You can mix typed and untyped code in the same file.

Unannotated code is implicitly treated as `Any`, which is compatible with everything. Static checkers generally skip it.

```python
from typing import Any

def typed(x: int) -> str:      # Checker watches this
    return str(x)

def untyped(x):                # x is implicitly Any
    return x.whatever_you_want # No error

# Explicit Any — same effect, but intent is clear
def explicit(x: Any) -> Any:
    return x
```


## 3. Optional and Union

`Union[X, Y]` means the value can be either `X` or `Y`.

`Optional[X]` is just shorthand for:

```python
Union[X, None]
```

### Modern Python (3.10+)

```python
from typing import Optional, Union

# These two signatures are identical:

def greet(name: Optional[str] = None) -> str:
    ...

def greet(name: str | None = None) -> str:
    ...
```

### Union Example

```python
def process(value: Union[int, str]) -> str:
    ...

def process(value: int | str) -> str:
    ...
```

### ⚠️ Common Trap

```python
def f(x: Optional[str]):
    ...
```

This **still requires** `x` to be passed.

To make it optional:

```python
def f(x: Optional[str] = None):
    ...
```


## 4. Generic Collections

Annotate what type of elements a collection holds.

Use built-in generics (`list`, `dict`, etc.) directly in Python 3.9+.

### Concrete Types

```python
names: list[str] = ["Alice", "Bob"]

scores: dict[str, int] = {
    "Alice": 95
}
```

### Abstract Types (Preferred for Parameters)

```python
from collections.abc import Sequence, MutableSequence

def total(nums: Sequence[float]) -> float:
    return sum(nums)
```

```python
total([1.0, 2.0])   # ✅ list
total((1.0, 2.0))   # ✅ tuple
```

### C++ Parallel

```cpp
std::vector<std::string>
```

is roughly:

```python
list[str]
```

Using `Sequence[str]` is similar to accepting a const reference to any compatible container rather than requiring a specific container type.


## 5. Tuple Types

Unlike lists, tuples:

* Can contain different types
* Have a fixed length (unless using `...`)

### Fixed Length

```python
point: tuple[int, str] = (1, "hello")
```

### Variable Length

```python
coords: tuple[float, ...] = (
    1.0,
    2.0,
    3.0
)
```

### Empty Tuple

```python
empty: tuple[()] = ()
```

### Common Use: Multiple Return Values

```python
def min_max(nums: list[float]) -> tuple[float, float]:
    return min(nums), max(nums)
```

### ⚠️ Common Trap

```python
tuple[int]
```

means:

```python
(42,)
```

Exactly **one** integer.

```python
tuple[int, ...]
```

means:

```python
(1, 2, 3, 4)
```

Any number of integers.


## 6. Generic Mappings

Annotate dictionaries with key/value types.

Prefer abstract types in function parameters.

```python
from collections.abc import Mapping, MutableMapping
```

### Concrete Type

```python
config: dict[str, int] = {
    "timeout": 30,
    "retries": 3
}
```

### Read-Only Access

```python
def get_timeout(cfg: Mapping[str, int]) -> int:
    return cfg["timeout"]
```

### Mutable Access

```python
def set_default(cfg: MutableMapping[str, int]) -> None:
    cfg.setdefault("retries", 3)
```


## 7. Iterable

Use `Iterable[T]` when a function only needs to loop through items.

```python
from collections.abc import Iterable

def print_all(items: Iterable[str]) -> None:
    for item in items:
        print(item)
```

Examples:

```python
print_all(["a", "b"])         # ✅ list
print_all(("a", "b"))         # ✅ tuple
print_all({"a", "b"})         # ✅ set
print_all(x for x in "ab")    # ✅ generator
```

### Flexibility Hierarchy

```text
Iterable
    ↓
Sequence
    ↓
MutableSequence
    ↓
list
```

Most flexible → least flexible


## 8. Literal

Restricts a parameter to exact values.

Useful as a lightweight enum.

```python
from typing import Literal

def open_file(
    path: str,
    mode: Literal["r", "w", "a"]
) -> None:
    ...
```

```python
open_file("data.txt", "r")  # ✅
open_file("data.txt", "x")  # ❌ mypy error
```

### Integers and Booleans

```python
def set_level(level: Literal[1, 2, 3]) -> None:
    ...
```

### C++ Parallel

Similar to limiting a parameter to specific enum values:

```cpp
enum class Mode {
    Read,
    Write,
    Append
};
```

But `Literal` avoids defining a full enum.


## 9. TypedDict

Gives a plain dictionary a fixed shape that static checkers understand.

At runtime it is still just a regular dictionary.

```python
from typing import TypedDict

class Movie(TypedDict):
    title: str
    year: int
    rating: float
```

### Usage

```python
movie: Movie = {
    "title": "Dune",
    "year": 2021,
    "rating": 8.0
}
```

```python
print(movie["title"])     # ✅

print(movie["director"])  # ❌ mypy error
```

### Runtime Reality

```python
isinstance(movie, dict)
# True
```

No class overhead.

### Optional Keys

```python
class Movie(TypedDict, total=False):
    title: str
    year: int
```

All keys become optional.

### C++ Parallel

Closest equivalent:

```cpp
struct Movie {
    std::string title;
    int year;
    float rating;
};
```

Unlike a C++ struct, `TypedDict` provides **no runtime enforcement**. It only helps static type checkers.


## Quick Mental Model

| Python Type          | Purpose                       | C++ Analogy          |
| -------------------- | ----------------------------- | -------------------- |
| `Any`                | Disable checking              | `void*`              |
| `Union`              | Multiple possible types       | `std::variant`       |
| `Optional[T]`        | `T` or `None`                 | Nullable pointer     |
| `Sequence[T]`        | Read-only sequence            | `const vector<T>&`   |
| `MutableSequence[T]` | Modifiable sequence           | `vector<T>&`         |
| `Iterable[T]`        | Anything iterable             | Range-based for-loop |
| `Literal[...]`       | Fixed values only             | Enum values          |
| `TypedDict`          | Typed JSON/dict shape         | Simple struct        |
| `tuple[T1, T2]`      | Fixed-size heterogeneous data | `std::tuple<T1, T2>` |

