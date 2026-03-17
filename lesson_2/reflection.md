
---

В данном уроке нам необходимо показать как работает наследование. Есть три варианта работы:
- расширение-родителя (добавление новых атрибутов и методов)
- специализация родителя (переопределение существующих методов и добавление атрибутов с целью сузить специальность до более конкретного типа)
- комбинация нескольких родительских классов (комбинирование классов в новом типе не только за счет наследования, но и композиции)

В схеме выглядит вот так:


![[resources/inheritance_types_diagram.svg]]
### Пример:

В данном примере показываем комбинированный случай, когда мы и расширяем класс родителя и делаем его более специализированным.

```python
class Document:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner
    
    def signature(self):
        print(f'подписан документ типа {self.type}')

class Contract(Document):
    def __init__(self, type, owner, parties):
        super().__init__(type, owner)
        self.parties = parties
    
    # наследник расширяет базовый класс родителя -> расширение класса-родителя
    def stamp(self):
        print('согласовано - поставлена печать')

class TaxBill(Document):
    def __init__(self, type, owner, departament):
        super().__init__(type, owner)
        self.departament = departament
    
    # наследник переопределяет родительский метод подписи, специализируя класс
    # -> специализация класса-родителя
    def signature(self):
        print('подписано электронной подписью')
```

## Рефлексия

---

Условно эталонный пример:

```python
class Bicycle: // велосипед
    def __init__(self, wheel_count: int = 2):
        self.wheels = [Wheel() for _ in range(wheel_count)]

class Engine: // электромотор
    def __init__(self, power: float):
        self.power = power
        print('engine power is', power)

# Специализация: шоссейный велосипед -- подтип велосипеда
# Расширение: электровелосипед, дополнен мотором
class ElectricRoadBicycle(Bicycle):
    def __init__(self, power: float):
        super().__init__()
        self.engine = Engine(power)
```

Проанализировав эталонный пример, понял, что он показывает комбинированный случай более явно, чем мой пример, хоть и я привел корректный случай. Также не совсе понятна специализация, так как у меня нет подтипа конкретного документа, например, подтип "Контракта". Попробуем исправить и сделать более явную версию:

```python
class Document:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner
    
    def signature(self):
        print(f'подписан документ типа {self.type}')

class Contract(Document):
    def __init__(self, type, owner, parties):
        super().__init__(type, owner)
        self.parties = parties
    
    # наследник расширяет базовый класс родителя -> расширение класса-родителя
    def stamp(self):
        print('согласовано - поставлена печать')

# приложеие к трудовому-договору
class Annex:
    def __init__(self, benefits):
        self.benefits = benefits

# условия труда
class WorkingConditions:
    def __init__(self, salary, working_hours, operating_mode):
        self.salary = salary
        self.working_hours = working_hours
        self.operating_mode = operating_mode

# расширение: трудовой договор дополнен методом, приложением к договору и рабочими условиями
# специализация: трудовой договор подтип контракта
class EmploymentContract(Contract):
    def __init__(self, type, owner, parties, conditions : WorkingConditions, annex : Annex):
        super().__init__(type, owner)
        self.parties = parties
        self.conditions = conditions
        self.annex = annex
    
    def stamp(self):
        print('согласовано - поставлена печать')
```

В новой версии четко прослеживается специализация "Контракта" и расширение "Документа"