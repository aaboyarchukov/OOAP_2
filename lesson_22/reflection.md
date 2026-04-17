# Классификация категорий наследования - 4

Продолжаем изучать категории наследования [прошлая часть](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_21/reflection.md)

### Категории наследования
---
9. Наследование вида - в данной категории мы используем наследовании при возникновении различных классификаций у сущности, среди которых нет явной главной

Проблема:
У главной доменной сущности есть характеристики, которые можно классифицировать, причем они активно комбинируются.

Например, есть базовый класс Сотрудник и у него может быть различная должность: Менеджер, Разработчик, Дизайнер, также у него может быть различные виды контрактов - Долгосрочный договор по ТК, Договор по ГПХ, Краткосрочный на оказание услуг и тд.
Проблема в том, как сочетать различные характеристики? Постоянный Дизайнер, Временный Программист?
Решение ->  нам будет лучше выделить отдельные иерархии - домены под выделенные классификации, которые можно через наследование комбинровать, а затем через полиморфизм и композицию - мы построим итоговую сущность:

```
class Договор: ...
class Должность: ...

class Постоянный(Договор): ...
class Программист(Должность): ...

class Сотрудник:
	договор Договор
	должность Должность
```

Такого наследования стоит придерживаться при следующих ситуациях:
- мы для конктретного класса можем выделить несколько классификаций одной характеристики, которые не статичны и среди них сложно выделить главную
- применяется активная комбинация выявленных классификаторов
- родительская сущность каждой их иерархий играет важную доменную роль и здесь нужно достаточно хорошо продумать АТД

### Пример
---

```python
class Actuator:

class MechanicActuator(Actuator): ...
class ElectricActuator(Actuator): ...
	
class RideType:

class MountingType(RideType):
	def mounting(self): ...
	
class WaterRidingType(RideType):
	def swim(self): ...

class Bycicle:
	def __init__(self, actuator : Actuator, ride_type : RideType):
		self.actuator = actuator
		self.ride_type = ride_type
	def ride(self):
		...
	def brake(self):
		...
```

### Рефлексия
---
Эталонное решение:

**Java**

```java
interface Material {
     // материал для шитья
    void sew();
}

class Wool implements Material {
    @Override
    public void sew() {}
}

class Cotton implements Material {
    @Override
    public void sew() {}
}

interface Clothes {
    // материалы, из которых изготовлена вещь
    Material[] getMaterials();

    // надеть одежду
    void putOn();
    int getSize();
    String getBrand();
}

class Blouses implements Clothes {
    private final Material[] materials;
    private final String brand;
    private final int size;

    public Blouses(Material[] materials, String brand, int size) {
        this.materials = materials;
        this.brand = brand;
        this.size = size;
    }

    @Override
    public Material[] getMaterials() {
        return new Material[0];
    }

    @Override
    public void putOn() {}

    @Override
    public int getSize() {
      return this.size;
    }

    @Override
    public String getBrand() {
        return this.brand;
    }
}

class Trousers implements Clothes {

    private final Material[] materials;
    private final String brand;
    private final int size;

    public Trousers(Material[] materials, String brand, int size) {
        this.materials = materials;
        this.brand = brand;
        this.size = size;
    }

    @Override
    public Material[] getMaterials() {
        return new Material[0];
    }

    @Override
    public void putOn() {}

    @Override
    public int getSize() {
        return this.size;
    }

    @Override
    public String getBrand() {
        return this.brand;
    }
}
```

Имеется класс "Одежда", от которого наследуются классы "Брюки" и "Блузки".  
Одежда предполагает несколько связанных сущностей, определяющих состояние вещи.  
В частности, одежда характеризуется формой и материалом, из которого она сделана. Оба этих признака часто используются вместе.  
Признак формы логично выделить основным: клиента интересует различие прежде всего между брюками и блузками, а не между материалами, из которых они сделаны.  
Поэтому признак материала выделен в отдельную иерархию -- он находится в отношении композиции с классом одежда (одежда содержит материал).

**Python**

```python
class Race():
    race_name = ''
    motherland = ''

class Elf(Race):
    race_name = 'elf'
    motherland = 'Nilfadiil'

class Orc(Race):
    race_name = 'orc'
    motherland = 'Grocks mountain'

#

class GameClass():
    def battle_method(self, target):
        raise NotImplementedError

class Wizard(GameClass):
    def battle_method(self, target):
        print(f'Phew-phew. Magick missle flying to {target}')

class Barbarian(GameClass):
    def battle_method(self, target):
        print(f'GRAAAA. My axe want to crack {target}\'s head!')

#

class Hero():
    def __init__(self, race, game_class):
        self.race = race
        self.game_class = game_class
```

Имеется класс Hero (Герой), у которого есть своя раса (бонусы к характеристикам и т.п.).  
У героя также имеется один из игровых классов (боеввые навыки и т.п.).  
Сперва напрашивается создать класс Wizard как наследник класса Hero, и дополнить атрибутом расы.  
Однако на курсе уже не раз отмечалось, что в подобной ситуации атрибуты будут плодить лишние условные цепочки.  
Поэтому создадим иерархию классов для характеристики расы и применим льготное наследование.

Так же применим наследование реализации и создадим иерархию классов для другой важной характеристики -- игрового класса.

Итог -- отдельный класс Hero, экземпляры которого содержат в себе классы Race и GameClass как атрибуты. Часто в игровых системах стартовые раса и класс определяют существенные бонусы и ограничения, накладываемые на игровой процесс, так что мы имеем несколько критериев классификации, как минимум одна из которых может меняться в течение игры (игровой класс). Race и GameClass в принципе равнозначны, и лучше добавлять их обоих композицией.

Проанализировав эталонное решение, понял, что пример необходимо дополнить описанием:

Класс Велосипед, который характеризуется определенным приводом и типом местности, для которой предназначен определенный велосипед. Так у нас может сочетаться тип Привода с определенным типом Поездки.

```python
class Actuator:

class MechanicActuator(Actuator): ...
class ElectricActuator(Actuator): ...
	
class RideType:

class MountingType(RideType):
	def mounting(self): ...
	
class WaterRidingType(RideType):
	def swim(self): ...

class Bycicle:
	def __init__(self, actuator : Actuator, ride_type : RideType):
		self.actuator = actuator
		self.ride_type = ride_type
	def ride(self):
		...
	def brake(self):
		...
```