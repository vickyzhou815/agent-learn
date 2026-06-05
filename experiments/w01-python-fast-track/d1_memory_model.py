# week1 - chapter 6 
# python's reference model

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
original = {"city": "Vancouver", "pop": 675000}
alias = original      # alias
alias["pop"] = 700000 # rebinding
print(original)       # {'city': 'Vancouver', 'pop': 700000} - original is modified because alias is a reference to the same dict object.
                      # alias and original share the same dict object.

copy = dict(original)    # shallow copy, creates a new dict object with the same key-value pairs
copy["city"] = "Toronto" # rebinding
print(original)          # {'city': 'Vancouver', 'pop': 700000} - original is unchanged because copy is a different dict object.

original = {"city": "Vancouver", "pop": 675000, "landmarks": ["Stanley Park", "Granville Island"]}
alias = original
alias["landmarks"].append("Capilano Suspension Bridge") # mutating the innerlist object
print(original)          # {'city': 'Vancouver', 'pop': 675000, 'landmarks': ['Stanley Park', 'Granville Island', 'Capilano Suspension Bridge']}
                         # original is modified because alias and original reference the same dict, and the list object in the 'landmarks' key is also shared.

# value types (mutable/immutable) inside don't matter for aliasing.
# shallow copy(dict(x), list[:], copy.copy()):
#   - Top level: new container object -> rebinding keys/indices is independent
#   - Inner values: still shared references -> this is where mutable vs immutable matters:
#     - Inner immutable (str, int, tuple) -> safe, because we can't mutate them in place, forced to rebind
#     - Inner mutable (list, dict) -> could be dangerous, in-place mutation affects original and copy.
#                                     rebinding a slot in the copy will not affect the original ('=').



# ============================================================
# 4. SHALLOW VS DEEP COPY
# ============================================================
roster = [["Alice", "Bill"], ["Carrie", "Dave"]]

shallow1 = copy.copy(roster)
shallow1[0].append("Eve")  # mutate
print(roster[0])           # ["Alice", "Bill", "Eve"] — inner list is shared, so original is modified

shallow2 = list(roster)    # also a shallow copy
shallow2[0] = ["Mike"]     # rebind
print(roster[0])           # ["Alice", "Bill", "Eve"] — unchanged, rebinding the slot in shallow2 does not affect roster  

deep = copy.deepcopy(roster)
deep[1].append("Frank")
print(roster[1])      # ["Carrie", "Dave"] — unchanged, deep copy creates new inner lists


# All of the following produce a shallow copy
# -------------------------------------------------------
# copy.copy(obj)  - Any object       - Generic, needs import
# lst.copy()      - list, dict, set  - Clean, idiomatic
# lst[:]          - Sequences only   - Old-school, pre-Python 3 habit
#                   (list, str, tuple)
# list(lst)       - Any iterable     - Also converts type
# -------------------------------------------------------

# for shallow copy, the outer container's slots are independent, but the inner lists are shared references in both shallow1 and shallow2
# can take it as:
#     original -> [ slot0 -> refA,  slot1 -> refB ]
#     copy     -> [ slot0 -> refA,  slot1 -> refB ]
# Slots are independent — reassigning copy[0] just makes copy's slot0 point somewhere else. Original's slot0 is untouched.
# The objects slots point to are shared — refB is the same object. Mutating it (append, update, etc.) is visible through both.



# ============================================================
# 5. MUTABLE DEFAULT ARGUMENT TRAP
# ============================================================
class HauntedBus:
    def __init__(self, passengers=[]):    # BUG!!!
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

bus1 = HauntedBus()
bus1.pick("Alice")
bus2 = HauntedBus()
print(bus2.passengers)      # ["Alice"] — ghost passenger!!!
print(bus1.passengers is bus2.passengers)  # True — same list object

# Inspect where the default lives:
print(HauntedBus.__init__.__defaults__)   # (['Alice'],) — stored on function object

# The above is quite different from C++ where default arguments are evaluated at the call site, 
# and each call gets a fresh default value. In Python, the default argument is evaluated once at function definition time, 
# and the same object is used for all calls that don't provide that argument.

class FixedBus:
    def __init__(self, passengers=None):    # FIXED
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)  # defensive copy, if not use copy here, could mutate the original list at call site, which might not be intended.

    def pick(self, name):
        self.passengers.append(name)

bus3 = FixedBus()
bus3.pick("Alice")
bus4 = FixedBus()
print(bus4.passengers)  # [] — clean slate
print(bus3.passengers is bus4.passengers)  # False — independent objects



