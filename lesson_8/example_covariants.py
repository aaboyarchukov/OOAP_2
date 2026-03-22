from typing import Generic, TypeVar

T = TypeVar('T', covariant=True)

# ковариативность с помощью обобщенного метода

class ContainerMap(Generic[T]):
    def __init__(self, item: T):
        self.item = item
    def get(self) -> T:
        return self.item

class Map:
    pass

class HashMap(Map):
    pass

class LinkedHashMap(HashMap):
    pass

def print_map(c : ContainerMap[Map]):
    print(c)

print_map(ContainerMap(Map()))
print_map(ContainerMap(HashMap()))
print_map(ContainerMap(LinkedHashMap()))

# ковариатиновость в фабриках
class MapFactory:
    def build_map(self) -> Map:
        return Map()
    
class HashMapFactory:
    def build_hash_map(self) -> HashMap:
        return HashMap()
    
class LinkedHashMapFactory:
    def build_linked_hash_map(self) -> LinkedHashMap:
        return LinkedHashMap()