# Пример динамического связывания и полиморфизма

### Динамическое связывание и полиморфизм
---
Как на прошлом занятии мы выяснили, что такое [[Класс как тип#Динамическое связывание|динамическое связывание]] и как оно проявляется, вкратце, с помощью динамического связывания, мы способны при определении переменной общего типа, менять тип динамиечски при инициализации тех типов, которые наследуют/имплементируют общий тип:

> Объект p имеет тип ParentList, объект l -- тип LinkedList, и объект t -- тип TwoWayList. Тогда в программе разрешены так называемые **полиморфные присваивания**:
> 
> p = l
> p = t

то есть при инициализации объектами другого типа, у нашего родительского объекта подставляется ссылка другого объекта и при вызове общего метода, вызовется не родительский, а именно метод объекта, которым иницилизировали родительский объект.


### Проблема
---
При построении иерархии классов, возникает проблема в том, что наследники становятся все более узконаправленными, родительские методы переопределяются, переиспользование снижается из-за узконаправленности.

Причем основная проблема в том, что одинаковые методы работают с разными типами, и для каждого он перелпределяется, хотя суть метода одна и та же.

> Не возникает никаких конфликтов с системой типов, однако эта система типов и никак нам не помогает в избегании дублирования кода (или как минимум, дублирования семантики).

То есть суть такова, что нам необходимо обобщать родительский метод, чтобы не переопределять его в потомках, каждый раз копируя логику.
### Ковариантность и контравариантность
---
Решение есть:

**Ковариативность** - случай, когда иерархия классов сохраняется, ребенок является потомком родителя, может общий метод переопределять более узкоспециализированным значением (производитель). Например, родительский метод возвращает значение типа родителя, а переопределенный метод у потомка тогда вернет тип потомка.

```python
class Animal:
	def get_animal(animal : Animal) -> Animal:
		# ...
		return

class Cat(Animal):
	def get_animal(cat : Cat) -> Cat:
		# ...
		return
```

Иерархия сохраняется, метод `get_animal(animal : Animal) -> Animal` может принимать всех потомков класса Animal.

То есть главную роль тут играют классы производители, например:

```python
class GenericContainer[Generic[T]]:
	def __init__(self, item : T):
		self.item = item
		
	def get(self) -> T:
		return self.item

animal_container : Container[Animal] = Container(Cat)
cat_container : Container[Cat]  = Container(Cat)
```

Здесь все соответствует иерархии.

То есть при ***ковариативности*** говорится всегда о ***произвеодителе***, отдается определенный тип и сохраняется иерархия!

Производитель с типом родителя принимает любой тип потомка

**Контрвариативность** - случай, когда идет реверсирование иерархии классов и более униваерсальный метод становится потомком более узконаправленного (потребитель).

Например:

```python
class Animal:
	#...

class Cat(Animal):
	#...

class Kitten(Cat):
	#...
```

иерархия такова:

```
Kitten
	^
	|
   Cat
	^
	|
Animal
```

создаем потребителей:

```python
def print_kitten_methods(kitten : Kitten):
	kitten.kitten_method()
	kitten.cat_method()
	kitten.animal_method()

def print_cat_methods(cat : Cat):
	kitten.cat_method()
	kitten.animal_method()

def print_animal_methods(animal : Animal):
	kitten.animal_method()
```

и напишем аггрегирующаую функцию:

```python
def print_defferent_animals(func : Caller[Kitten], kitten : Kitten):
	func(kitten)

kitten = Kitten()

print_defferent_animals(print_kitten_methods, kitten)
print_defferent_animals(print_cat_methods, kitten)
print_defferent_animals(print_animal_methods, kitten)
```

о вызову можно понять, что иерархия изменилась и теперь `kitten` стоит во главе, то есть:

```
Caller[Animal]
	^
	|
Caller[Cat]
	^
	|
Caller[Kitten]
```

То есть при ***контрвариативности*** говорится всегда про ***потребителя***!

**Subtyping** подход - соответствие подтипов, то есть типы находятся строго в иерархии:

`Cat ЯВЛЯЕТСЯ Animal`

Здесь говорится просто о типах, и не иметтся в виду функции и контейнеры

### Примеры
---

Похожие примеры на Go сложно привести, поэтому приведу на python:

```python
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

class LinkedHashMap(Map):
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
```

```python
from typing import Callable

# контрвариативность через функции делегирования
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
```