
1. variables are just lables hold references to objects.
2. '==' compare equality (data), 'is' compare identity (memory address), alias
3. turple's relative immutability
4. copies are shallow by default. l2 = list(l1) / l2 = l1[:], the outermost container is duplicated but the copy is filled with references to the same items held by the original container
5. copy module ( copy, deepcopy)
6. call by sharing - function parameters as references, parameter inside the function become alias of the actual arguments. for immutable types of parameter, if for '+=', rebinding may break the alias.
7. mutable types as paramter may be a bad idea. if not passed (default [], this paramter is bound to the default list object which is empty), later even create multiple instances (objects) they share the some. this is quite different from C++.
8. for mutable parameter types, use: passenger = None,  in 'else': self.passenger = list(passengers) - make a copy, even though it's a shallow copy, it creates a new container, the string obj references in the container are shared. (as long as will not change the inner mutable obj, otherwise will affect the original as wee)
9. 'del' delete references, not objects. garbage collection - reference counting. (any difference with c+++? not sure yet)
10. for turple (immutable), t[:] and turple(t) does not make a copy, but returns a reference to the same object.
11. Augmented assignment with += or *= creates new objects if the lefthand variable is bound to an immutable object, but may modify a mutable object in place.