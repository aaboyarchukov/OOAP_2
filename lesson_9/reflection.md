# Общая структура иерархии классов в проекте

### Иерархия классов в проекте
---

При построении программы - наша задача состоит в том, чтобы организовать грамотную иеррахию классов - где в самом верху будет класс определяющий общие методы, не поддающиеся изменениям. От этого класса наследуются все объекты программы (неявно), например, как `object` в Java/C#.

Такой класс должен реализовывать базовые операции, такие как:

-- **копирование объекта** (копирование содержимого одного объекта в другой существующий, включая DeepCopy -- глубокое рекурсивное дублирование, подразумевающее также копирование содержимого объектов, вложенных в копируемый объект через его поля, атрибуты);   
-- **клонирование объекта** (создание нового объекта и глубокое копирование в него исходного объекта);  
-- **сравнение объектов** (включая глубокий вариант);  
-- **сериализация/десериализация** (перевод в формат, подходящий для удобного ввода-вывода, как правило в строковый тип, и восстановление из него);  
-- **печать** (наглядное представление содержимого объекта в текстовом формате);  
-- **проверка типа** (является ли тип текущего объекта указанным типом);   
-- **получение реального типа объекта** (непосредственного класса, экземпляром которого он был создан).

Ну при добавлении нового класса, мы наследуем его от самого верхнего в иерархии, но не того, который недоступен к изменениям, а тот кто открыт. То есть:

```python
# мы обозначаем клас General, который закрыт к изменениям
# и определяет основные операции

# закрытый для изменений
class General(object):
	pass
	
# но от него наследуем другой класс, который будет открыт для изменений

# открытый для изменений
class Any(General):
    pass
    
# и вот уже новые классы будут унаследованы от Any
```

Вот как должны выглядеть классы:

```python
from typing import TypeVar
from copy import deepcopy
import json

T = TypeVar('T', covariant=True)

# закрытый для изменений
class General(object):

    # обход всех аттрибутов внутри объекта и копирование их в текущий
    def copy(self, obj_from : T):
        if not (type(self) is type(obj_from)):
            return
        
        attributes = vars(obj_from)
        for attr in attributes:
            target = getattr(obj_from, attr)
            setattr(self, attr, deepcopy(target))
    
    # возвращает результат copy
    def clone(self, obj_from : T) -> T:
        return self.copy(obj_from)

    def __eq__(self, target) -> bool:
        if type(self) is type(target):
            return False
        
        target_attributes = vars(target)
         
        for attr in target_attributes:
            
            target_val = getattr(target, attr)
            self_val = getattr(self, attr)
            
            # сравнение будет корректно, так как
            # я переопределяю именно метод __eq__,
            # а значит он будет автоматически переопределен для потомков
            if target_val != self_val:
                return False
            
        return True

    # перевод аттрибутов в строку json
    def serialize(self):
        return json.dumps(vars(self))

    # перевод из строки в аттрибуты текущего объекта
    def deserialize(self, target_row : str):
        target_dict : dict = json.loads(target_row)
        for attr, value in target_dict.items():
            setattr(self, attr, value)

    # вывод всех аттрибутов (лучше переопределить __str__, чем использовать print)
    def __str__(self):
        print(
            str(vars(self))
        )

    def check_type(self, target_type : T) -> bool:
        return type(self) is target_type

    def type(self) -> T:
        return self.__class__

# открытый для изменений
class Any(General):
    pass
```