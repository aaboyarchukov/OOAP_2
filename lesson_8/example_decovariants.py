from typing import Callable

class Map:
    def map_method(self):
        pass

class HashMap(Map):
    def hash_map_method(self):
        pass

class LinkedHashMap(HashMap):
    def linked_hash_map_method(self):
        pass

def print_map_methods(m : Map):
    m.map_method()

def print_hash_map_methods(hm : HashMap):
    hm.map_method()
    hm.hash_map_method()

def print_linked_hash_map_methods(lhm : LinkedHashMap):
    lhm.map_method()
    lhm.hash_map_method()
    lhm.linked_hash_map_method()

def print_methods_of_maps(func : Callable[[LinkedHashMap]], m : LinkedHashMap):
    func(m)

lhm = LinkedHashMap()

print_methods_of_maps(print_map_methods, lhm)
print_methods_of_maps(print_hash_map_methods, lhm)
print_methods_of_maps(print_linked_hash_map_methods, lhm)

