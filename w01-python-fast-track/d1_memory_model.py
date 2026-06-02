# week1 - chapter 6 
# python's reference model vs C++ value semantics

# ============================================================
# 1. VARIABLES ARE NOT BOXES — they are labels/references
# ============================================================
a = [1, 2, 3]
b = a         # b is not a copy, but a reference to the same list object
b.append(4)   # modifying b also modifies a, since they reference the same list
print(a)      # [1, 2, 3, 4]
print(a is b) # True

# In python, assignment is always just binding a name to an object - it never copies the object. This is different from C++ where assignment can involve copying values.
# In some cases, "immutables feel like copies" illusion may come from the fact that we can't mutate them in-place
#  — any operation that would change the value instead produces a new object and rebinds the variable. 
# The assignment itself was still just an alias.
a = 42
b = a
b = b + 1      # create a new int object and rebinds b
print(a)       # 42
print(b)       # 43
print(b is a)  # False




# ============================================================
# 2. is vs ==
# ============================================================
x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)   # True
print(x is y)   # False, because x and y are different objects in memory

# '==' compares values (content), while 'is' compares identities (memory addresses)

# ============================================================
# 3. REFERENCE ALIASING WITH A DICT
# ============================================================
