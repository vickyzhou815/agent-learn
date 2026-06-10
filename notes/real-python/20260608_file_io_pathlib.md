
Ref Pathlib: https://realpython.com/python-pathlib/


# Python `pathlib` Module — Summary

## Why `pathlib`?

Before `pathlib`, file path handling was scattered across `os`, `glob`, and `shutil`, requiring multiple imports for even basic operations. `pathlib` brings this functionality together and provides a `Path` object — a cross-platform, object-oriented way to read, write, move, and delete files.

**Old way:**
```python
import glob, os, shutil
for f in glob.glob("*.txt"):
    shutil.move(f, os.path.join("archive", f))
```

**`pathlib` way:**
```python
from pathlib import Path
for f in Path.cwd().glob("*.txt"):
    f.replace(Path("archive") / f.name)
```


## Creating `Path` Objects

Three ways to instantiate:

```python
from pathlib import Path

Path.cwd()           # current working directory → WindowsPath or PosixPath
Path.home()          # user's home directory
Path("/some/dir")    # from a string (use raw strings r"..." on Windows)
Path(__file__).parent  # relative to the current script
```

**Joining paths** — use the `/` operator (overloaded, not division):
```python
Path.home() / "projects" / "myfile.py"
Path.home().joinpath("projects", "myfile.py")  # equivalent
```

`Path` auto-selects `WindowsPath` or `PosixPath` at runtime — write once, run anywhere.


## Path Component Properties

```python
p = Path("/home/user/realpython/test.md")

p.name      # "test.md"         — full filename
p.stem      # "test"            — name without extension
p.suffix    # ".md"             — just the extension
p.anchor    # "/"               — root
p.parent    # PosixPath("/home/user/realpython")
p.parent.parent  # chainable
```


## Reading & Writing Files

```python
# Read
text = Path("file.md").read_text(encoding="utf-8")
data = Path("file.bin").read_bytes()

# Write (overwrites silently — be careful!)
Path("out.md").write_text("hello", encoding="utf-8")
Path("out.bin").write_bytes(b"\x00\xff")

# Or use open() directly on a Path
with Path("file.md").open(mode="r", encoding="utf-8") as f:
    content = f.read()
```


## Renaming Files

```python
p = Path("/home/user/hello.txt")

p.with_suffix(".md")         # change extension only → hello.md
p.with_name("goodbye.md")    # change full filename  → goodbye.md
p.with_stem("world")         # change stem only      → world.txt

# Actually rename on disk:
p.replace(p.with_suffix(".md"))
```

## Copying Files

`Path` has no built-in copy method — use read/write:
```python
src = Path("shopping_list.md")
dst = src.with_stem("shopping_list_backup")
dst.write_bytes(src.read_bytes())
```
Or use `shutil`, which also accepts `Path` objects.


## Moving & Deleting Files

```python
# Move / rename (overwrites destination if it exists)
Path("hello.py").replace(Path("goodbye.py"))

# Safe move — avoid race condition with exclusive open
with destination.open(mode="xb") as f:  # "x" = fail if exists
    f.write(source.read_bytes())
source.unlink()   # delete source after successful copy

# Delete a file
Path("old.txt").unlink()
```


## Creating Empty Files

```python
f = Path("hello.txt")
f.touch()                    # creates if missing, updates mtime if exists
f.touch(exist_ok=False)      # raises FileExistsError if already present
```


## Listing & Searching Files

```python
Path.cwd().iterdir()         # all entries in directory (files + dirs)
Path.cwd().glob("*.txt")     # pattern match in current dir
Path.cwd().rglob("*.py")     # recursive glob into subdirectories
```

**Count by extension:**
```python
from collections import Counter
Counter(p.suffix for p in Path.cwd().iterdir())
# Counter({'.txt': 4, '.md': 2, '.py': 1})
```


## Practical Examples

**Most recently modified file:**
```python
from datetime import datetime
t, path = max((f.stat().st_mtime, f) for f in Path.cwd().iterdir())
print(datetime.fromtimestamp(t), path)
```

**Unique filename generator:**
```python
def unique_path(directory, pattern):
    counter = 0
    while True:
        counter += 1
        p = directory / pattern.format(counter)
        if not p.exists():
            return p

unique_path(Path.cwd(), "test{:03d}.txt")  # → test003.txt (if 001,002 exist)
```

**Directory tree:**
```python
def tree(directory):
    print(f"+ {directory}")
    for p in sorted(directory.rglob("*")):
        depth = len(p.relative_to(directory).parts)
        print("    " * depth + f"+ {p.name}")
```


## Quick Reference

| Task | Method/Property |
|---|---|
| Current dir | `Path.cwd()` |
| Home dir | `Path.home()` |
| Join paths | `p / "subdir"` or `.joinpath()` |
| Read text | `.read_text(encoding=...)` |
| Write text | `.write_text(data, encoding=...)` |
| Rename/move | `.replace(new_path)` |
| Delete | `.unlink()` |
| Exists? | `.exists()` |
| Is file? | `.is_file()` |
| Is dir? | `.is_dir()` |
| List dir | `.iterdir()` |
| Glob | `.glob("*.py")` |
| Recursive glob | `.rglob("*.py")` |
| File metadata | `.stat().st_mtime` |
| Create empty file | `.touch()` |


**C++ mental model bridge:** Think of `Path` like a smart wrapper around a `std::filesystem::path` (C++17). The `/` operator is operator overloading — analogous to how C++ overloads `<<` for streams. `PurePath` vs `Path` maps roughly to a value-semantic path string vs one that also carries OS syscall capability.