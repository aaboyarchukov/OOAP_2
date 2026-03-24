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

### Рефлексия
---

Эталонное решение:

Пример 1:

```python
#ковариантность

from typing import Generic, TypeVar, Callable

animal = TypeVar('animal', covariant=True)

class Animal(): pass
class Cat(Animal): pass

# Контейнер на вход принимает любой объект типа Anuimal
class Box(Generic[animal]):
    def __init__(self, content: animal) -> None:
        self._content = content

# Можно проверить контейнер с животным, 
# а значит, и с котом, как частным случаем животного
def check_box(box: Box[Animal]):
    pass

box = Box(Cat())
check_box(box)
```

```python
#контравариантность

class Person(): pass
class Sportsman(Person): pass
class Policeman(Person): pass

def person_run(person: Person) -> None:
    print('Person running')

# Спортсмен и полисмен могут бегать: 
def sportsman_run(sportsman: Sportsman) -> None:
    print('Sportsman running. So fast!')
def policeman_run(policeman: Policeman) -> None:
    print('The policemen don\'t run. He shoots.')

# ковариантным типом по документации считается Callable
def make_sportsman_run(sportsman: Sportsman, run_func: Callable[[Sportsman], None]):
    print('Shoot in the air with gun!')
    run_func(sportsman)

# подойдёт даже обычный Person
make_sportsman_run(Sportsman(), person_run)

# а вот на типе Policeman будет ошибка
make_sportsman_run(Sportsman(), policeman_run)
```

Пример 2:

```python
# ковариантность

class Sword: pass
class FuryBlade(Sword): pass

class Knight:
    def get_melee_weapon(self):
        return Sword()
class Paladin(Knight):
    def get_melee_weapon(self):
        return FuryBlade()

knigt, paladin = Knight(), Paladin()
s, fb = knigt.get_melee_weapon(), paladin.get_melee_weapon()

isinstance(s, Sword), isinstance(s, FuryBlade)
# (True, False)

isinstance(fb, Sword), isinstance(fb, FuryBlade)
# (True, True)
```

```python
# контравариантность

from typing import TypeVar, Generic

T_contra = TypeVar('T_contra', contravariant=True)

class _T(Generic[T_contra]):
    def __init__(self, item: T_contra) -> None: ...

class BladedWeapon: pass
class Sword(BladedWeapon): pass
class Broadsword(Sword): pass
class Cutlass(Broadsword): pass
class Shuriken(BladedWeapon): pass

def sharpen_melee_weapon(weapon: _T[Broadsword]) -> None: pass

sword1, sword2 = _T(Broadsword()), _T(Sword())
sharpen_melee_weapon(sword1)  # OK
sharpen_melee_weapon(sword2)  # OK

shuriken = _T(Shuriken()) 
# error: "sharpen_melee_weapon" has incompatible type _T[Shuriken]
sharpen_melee_weapon(shuriken) # error

cutlass = _T(Cutlass()) # error ...
sharpen_melee_weapon(cutlass) # error
```

```java
// Ковариантность:
List<Integer> l1 = new ArrayList<>();
l1.add(42);
List<? extends Number> l2 = l1; // read-only список. 
// Безопасное приведение потомка(Integer) к родителю (Number)


// Контравариантность:
List<Number> l3 = new ArrayList<>();

List<? super Double> l4 = l3; // write-only список. 
// Безопасное приведение родителя (Number) к потомку (Double)

// Такой механизм позволяет обходить небезопасное приведение типов,
// когда в List<Double> могут оказаться значения типа Integer, 
// если сначала List<Double> привести к List<Number>
```

Проанализировав эталонное решение, понял, что на примерах показал явную разницу между ковариативностью и контрвариативностью.

Также в моих примерах можно было построить более сложную иерархию классов, чтобы на более трудном и не таком ясном примере понять различия двух подходов.