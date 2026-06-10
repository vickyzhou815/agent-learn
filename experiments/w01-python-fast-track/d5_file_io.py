# Instaniate
from pathlib import Path

Path.cwd()
Path.home()
Path('/Users/vickyzz/Documents/02_Dev/AI/projects/agent-learn')
Path(__file__).parent


# Join paths - use / operator (overloaded)
Path.home() / 'Documents' / '02_Dev' / 'AI' / 'projects' / 'agent-learn' / 'notes' / '20260608_file_io_pathlib.md'  # equivalent
Path.home().joinpath('Documents', '02_Dev', 'AI', 'projects', 'agent-learn', 'notes', '20260608_file_io_pathlib.md')  # quivalent
# Path auto selects windowpath or posixpath based on the OS at runtime


# Path components properties
p = Path("/Users/vickyzz/Documents/02_Dev/AI/projects/agent-learn/notes/20260608_file_io_pathlib.md")

p.name      # "test.md"         — full filename
p.stem      # "test"            — name without extension
p.suffix    # ".md"             — just the extension
p.anchor    # "/"               — root
p.parent    # PosixPath("/home/user/realpython")
p.parent.parent  # chainable


# Reading and writing files
# Read
# text = Path("/Users/vickyzz/Documents/02_Dev/AI/projects/agent-learn/notes/20260608_file_io_pathlib.md").read_text(encoding="utf-8")
base_dir = Path(__file__).parent.parent
dest_file = base_dir / "notes" / "20260608_file_io_pathlib.md"
text = dest_file.read_text(encoding="utf-8")
# read_bytes() for binary files

# Write
# overwrites silently, no error if file exists
# dest_file.write_text(text, encoding="utf-8")
# dest_file.write_bytes(data)  # for binary files

# or use open() with pathlib
with Path("file.md").open("r", encoding="utf-8") as f:
    text = f.read()


# Renaming files
p = Path("/home/user/realpython/hello.txt")

p.with_suffix(".md")    # change extension only
p.with_name("world.md") # change name and extension
p.with_stem("greet")    # change name only, keep extension
# the above methods return new Path objects, they do not modify the original path
# p.rename(p.with_suffix(".md"))  # actually rename the file on disk

p.replace(p.with_suffix(".md"))  # same as rename but raises error if destination exists


# Copying files
# Path has no built-in copy method, use read/write
src = Path("test.txt")
dest = Path("test_copy.txt")
dest.write_bytes(src.read_bytes())
# or use shutil


# Create empty file
f = Path("empty_file.txt")
f.touch()  # creates empty file if it doesn't exist, updates timestamp if it does
f.touch(exist_ok=False)  # raises error if file exists


# Listing & Searching files
Path.cwd().iterdir()     # generator of all files and directories in current directory
Path.cwd().glob("*.md")  # generator of all .md files in current directory
Path.cwd().rglob("*.md") # generator of all .md files in current directory and subdirectories
