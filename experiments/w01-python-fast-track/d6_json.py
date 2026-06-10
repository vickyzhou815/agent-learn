# s = string
# Python object -> json.dumps() -> json string    [in-memory]
# Python object -> json.dump()  -> json file      [on-disk]
# json string   -> json.loads() -> Python object  [in-memory]
# json file     -> json.load()  -> Python object  [on-disk]


# ---------------------------------------------------------------------------------
# Json.dumps() - encodes a Python object into a JSON string
# takes any serializable Python object, returns a str. Nothing touches the disk
# ---------------------------------------------------------------------------------
import json

data = {
    "name": "Vicky",
    "scores": [98, 87, 100],
    "active": True,
    "bonus": None
}

# Basic
print(json.dumps(data))

# Pretty print
print(json.dumps(data, indent=4))

# Sorted keys (great for tests & diffs)
print(json.dumps(data, sort_keys=True, indent=4))


# ---------------------------------------------------------------------------------
# Json.dump() - write directly to a file
# streams to a file-like object. work with open() or a Path in real cases
# ---------------------------------------------------------------------------------
# write to disk
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

# or with pathlib (they are the same)
from pathlib import Path
# first dump to a string, then write to file, but it's not recommended for large data
# Path("data2.json").write_text(json.dumps(data, indent=4))
with Path("data2.json").open("w") as f:
    json.dump(data, f, indent=4)


# ---------------------------------------------------------------------------------
# Json.loads() - decodes a JSON string into a Python object
# takes a JSON str, bytes, or bytearray, returns a Python object
# ---------------------------------------------------------------------------------
import json

# typical api response as a string
raw = '{"status": "ok", "count": 42, "items": ["apple", "banana", "cherry"], "meta": null}'
obj = json.loads(raw)

print(type(obj))            # <class 'dict'>
print(obj["status"])        # ok
print(obj["count"] + 1)     # 43  (it's an int, not a string!)
print(obj["items"][0])      # a
print(obj["meta"] is None)  # True

# ---------------------------------------------------------------------------------
# Json.load() - read directly from a file
# reads from a file-like object, returns a Python object
# ---------------------------------------------------------------------------------
with open("data.json", "r") as f:
    data_from_file = json.load(f)
    print(type(data_from_file)) # <class 'dict'>
    print(data_from_file)       # {'name': 'Vicky', 'scores': [98, 87, 100], 'active': True, 'bonus': None}


"""
Type Conversion Table (Python ↔ JSON)

What Python types map to JSON types, and what comes back when decoded.
Some conversions are not reversible (lossy or unsupported).

+------------+--------------------+----------------+----------------------+
| Python     | JSON wire format   | Decoded Python | Round-trip safe?     |
+------------+--------------------+----------------+----------------------+
| dict       | {"key": ...}       | dict           | yes                  |
| list       | [...]              | list           | yes                  |
| tuple      | [...]              | list           | no (tuple → list)    |
| str        | "..."              | str            | yes                  |
| int        | 42                 | int            | yes                  |
| float      | 3.14               | float          | yes (usually)        |
| bool       | true / false       | bool           | yes                  |
| None       | null               | None           | yes                  |
| set        | (not supported)    | -              | raises TypeError     |
| bytes      | (not supported)    | -              | raises TypeError     |
| datetime   | (not supported)    | -              | raises TypeError     |
+------------+--------------------+----------------+----------------------+
"""
import json
from datetime import datetime

data = {
    "event": "wafer_start",
    "timestamp": datetime(2026, 6, 10, 9, 30, 0),
    "lot_id": 42
}

def custom_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat() # Convert datetime to ISO string
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

print(json.dumps(data, default=custom_encoder, indent=4))


"""
Key Optional Parameters (JSON / Python json module)

All parameters below are keyword-only and shared across:
- json.dump()
- json.dumps()
- json.load()
- json.loads()

------------------------------------------------------------
indent=N
------------------------------------------------------------
Pretty-print JSON with N spaces per level.
- indent=2 or indent=4 are most common
- indent=None (default) → compact single-line output

------------------------------------------------------------
sort_keys=True
------------------------------------------------------------
Sort dictionary keys alphabetically.
- Makes output deterministic
- Useful for unit tests (assertEqual)
- Useful for clean git diffs

------------------------------------------------------------
separators=(',', ':')
------------------------------------------------------------
Controls item and key separators in JSON output.

Default is:
    (', ', ': ')

Compact version:
    (',', ':')

Use this for:
- smaller payloads
- network transmission
- minified JSON

------------------------------------------------------------
ensure_ascii=False
------------------------------------------------------------
Default is True → non-ASCII becomes escaped (\uXXXX)

If False:
- keeps UTF-8 characters as-is
- smaller output
- more human-readable (recommended for modern apps)

------------------------------------------------------------
default=fn
------------------------------------------------------------
Serialization fallback function for non-JSON types.

Used when json encounters unsupported objects like:
- datetime
- pathlib.Path
- Decimal
- custom classes

Function must:
- return JSON-serializable value OR
- raise TypeError

------------------------------------------------------------
object_hook=fn
------------------------------------------------------------
Deserialization hook (decode side).

Called for every JSON object (dict) during loading.

Use cases:
- convert dict → custom class
- reconstruct datetime / structured objects
- custom deserialization pipelines
"""


# ---------------------------------------------------------------------------------
# Gotachas
# ---------------------------------------------------------------------------------
# Dict keys are always coerced to strings in JSON. If you use non-string keys in Python, 
# they will be converted to strings when encoded, and will not be the same type when decoded.
import json

d = {1: "one", 2: "two", 3: "three", 4: "four"}
encoded = json.dumps(d)
print(encoded)          # {"1": "one", "2": "two", "3": "three", "4": "four"}

decoded = json.loads(encoded)
print(decoded)          # {'1': 'one', '2': 'two', '3': 'three', '4': 'four'}
print(type(decoded))    # <class 'dict'>

