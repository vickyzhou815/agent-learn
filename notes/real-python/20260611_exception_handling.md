
# Exception


### 1. The Hierarchy

```
BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
```

**The key insight:** catching a parent class also catches all its subclasses. So `except LookupError` catches both `IndexError` and `KeyError`. This is exactly like catching a base class exception in C++ — same polymorphism.



### 2. The `BaseException` vs `Exception` split — critical

`KeyboardInterrupt` inherits from `BaseException` so it won't be accidentally caught by code that catches `Exception`. This is intentional design. If you write `except Exception`, Ctrl+C still kills your program. If you write `except BaseException`, you'd trap it — almost never what you want.

**Rule:** always catch `Exception` or a subclass, never `BaseException`, unless you know exactly why.



### 3. The exceptions you'll see daily

| Exception | When it fires |
|---|---|
| `TypeError` | wrong type — `"a" + 1`, or calling non-callable |
| `ValueError` | right type, bad value — `int("abc")`, `math.sqrt(-1)` |
| `KeyError` | missing dict key |
| `IndexError` | list index out of range |
| `AttributeError` | accessing `.something` that doesn't exist |
| `NameError` | using a variable before assigning it |
| `ImportError` / `ModuleNotFoundError` | bad `import` |
| `OSError` / `FileNotFoundError` | file I/O problems |
| `StopIteration` | iterator protocol exhausted (rarely caught manually) |
| `NotImplementedError` | abstract base class method not overridden |



### 4. One practical pattern — catch specific, not broad

```python
# Bad (hides bugs):
try:
    data = config['key']
except Exception:
    data = default

# Good:
try:
    data = config['key']
except KeyError:
    data = default
```

Catching broad exceptions is like catching `...` in C++ — you lose all diagnostic information.



## Defer

- `__context__`, `__cause__`, `raise X from Y` — exception chaining. Useful when wrapping exceptions in library code, but not beginner-critical.
- `ExceptionGroup` — Python 3.11+, for async/concurrent error handling. Skip for now.
- All the `Warning` subclasses — a separate system, rarely caught directly.
- `__slots__` memory layout caveats for subclassing — implementation detail.

