# week1 - chapter 8 
# type hints in functions

# ============================================================
# 1. OPTIONAL, UNION, LITERAL — annotate a real function
# ============================================================
from typing import Optional, Union, Literal

# --- Union ---
# Union[X, Y] means the value can be either of type X or type Y
# Modern syntax: X | Y (Python 3.10+), same meaning as Union[X, Y], but no import needed

def stringify(value: Union[int, float, str]) -> str:
    return f"value is: {value}"

print(stringify(42))
print(stringify(3.14))
print(stringify("hello"))

# Modern equivalent:
def stringify_modern(value: int | float |str) -> str:
    return f"value is: {value}"

# --- Optional ---
# Optional[X] is just a shorthand for Union[X, None], meaning the value can be of type X or None
# These three are equivalent:
def greet_a(name: Optional[str] = None) -> str: ...    # old style
def greet_b(name: Union[str, None] = None) -> str: ... # explicit
def greet_c(name: str | None = None) -> str: ...       # modern (preferred)

# --- Literal ---
# Resricts to specific literal values, not just a type
# Used for flags, modes, or fixed-choice parameters
def format_name(first: str, last: str, title: Literal["Mr.", "Ms.", "Dr."] | None = None) -> str: # the first 'None' is for optional title, could be None, the second 'None' is default value.
    if title is None:
        return f"{first} {last}"
    else:
        return f"{title} {first} {last}"

print(format_name("John", "Doe"))                    # John Doe
print(format_name("Jane", "Smith", title="Dr."))     # Dr. Jane Smith
print(format_name("Alice", "Johnson", title="Prof")) # Error: Argument 'title' has incompatible type "Literal['Prof']"; expected "Union[Literal['Mr.'], Literal['Ms.'], Literal['Dr.'], None]"


# ============================================================
# 2. GENERIC COLLECTIONS — Sequence[float] vs list[float]
# ============================================================
# Sequence[T] is an abstract type that includes any ordered collection of T (like list, tuple, etc.)
# list[T] is a concrete type that specifically means a list of T
# TypedDict use 'class' syntax, but it's not a class in the OOP sense, it's just a way to define a dict with specific keys and value types, useful for structured data.

from collections.abc import Sequence  # abc -> Abstract Base Classes, represents objects that behave like a sequence (list, tuple, string, etc.)
from typing import TypedDict

class CourseReport(TypedDict):
    course_name: str
    num_students: int
    average_grade: float
    passed: bool

def generate_report(course_name: str, grades: Sequence[float]) -> CourseReport:
    return {
        "course_name": course_name,
        "num_students": len(grades),
        "average_grade": sum(grades) / len(grades) if grades else 0.0,
        "passed": all(grade >= 60 for grade in grades) # built-in all() function returns True if all elements of the iterable are true (or if the iterable is empty)
    }

print(generate_report("Math 101", [85.0, 92.5, 78.0, 60.0, 55.0]))    # {'course_name': 'Math 101', 'num_students': 5, 'average_grade': 74.1, 'passed': False}
print(generate_report("Physics 101", (88.0, 91.0, 76.0, 65.0, 58.0))) # works with turple as well
print(generate_report("History 201", []))  # Edge case. {'course_name': 'History 201', 'num_students': 0, 'average_grade': 0.0, 'passed': True} (no failing grades)


# ============================================================
# 3. TUPLE RETURN TYPES
# ============================================================
# --- tuple object literal ---
a = (3.14, True) # create a tuple object 
print(a)         # (3.14, True)

# --- tuple packing ---
b = 3.14, True   # packing: multiple values are packed into a single tuple object
print(b)         # (3.14, True)

# --- tuple constructor ---
c = tuple([3.14, True]) # calls the tuple class constructor. It takes an iterable (like a list) and returns a tuple containing the same elements.
print(c)                # (3.14, True)

# --- type annotation ---
d: tuple[float, bool]   # this does not create a tuple object, it's just a type annotation that says d should be a tuple containing a float and a bool.

def parse_date(date_str: str) -> tuple[int, int, int]:
    parts = date_str.split("-")
    return int(parts[0]), int(parts[1]), int(parts[2]) # this is tuple packing, the three ints are packed into a single tuple object that is returned.

year, month, day = parse_date("2026-06-01")  # tuple unpacking
print(year, month, day)                      # 2026 6 1


# mixed types in a tuple
def clamp(val: float, lo: float, hi: float) -> tuple[float, bool]:
    # Returns (clamped_value, was_clamped)
    # tuple[float, bool] — two elements of different types, like a struct in C++
    if val < lo:
        return lo, True
    if val > hi:
        return hi, True
    return val, False
 
print(clamp(5.0, 0.0, 10.0))               # (5.0, False) — within range, no clamping
print(clamp(-3.0, 0.0, 10.0))              # (0.0, True)  — clamped to lo
print(clamp(15.0, 0.0, 10.0))              # (10.0, True) — clamped to hi
 
# Note: tuple[float, ...] with ... means variable-length tuple of floats (like a list)
#       tuple[float, bool] means exactly 2 elements of those specific types
#       They are NOT the same
