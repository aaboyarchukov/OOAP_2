# Решение конфликта таксономии

### Конфликт таксономии
---
**Таксономия** - это практика классификации объектов по группам.

И при такой практике важно грамотно уметь расширять иерархию, здесь есть правило:

> 	**Добавление нового класса как потомка некоторого класса имеет смысл, если этот потомок либо переопределяет какие-либо наследуемые методы, либо расширяет его новыми методами**.

Но такж есть частный случай, когда неоходимо расширить класс, ничего не изменяя. Например, мы хотим добавить в наш класс `Human` атрибут `female` для отображения определенного пола. Но такой вариант является плохим потому, что от этого атрибута зависит дальнейшая логика, будет увеличиваться ветвление, а также повышаться цикломатическая сложность.

Чтобы это избежать, необходимо расширять классовую иерархию классами и переопределять методы, тогда у нас просто вместо сравнений будет простой вызов метода.
### Пример
---
[example.py](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_15/example.py)

```python
# при таком построении возникнут трудности и цикломатическая сложность будет расти
# так как от type ветвится логика
# class Bike:
#     def __init__(self, type, engine):
#         self.type = type
#         self.engine = engine

class Bike:
    def __init__(self, engine):
        self.engine = engine # будет композиция

class ElectricBike(Bike):
    pass

class BikeWithWings(Bike):
    pass

# но еще лучше здесь использовать паттерн Strategy с поведенческими классами
```

### Рефлексия
---
Эталонное решение:

**Python**

```python
class _ClassificationDataInput(Any):
    def get_prepared(self, *args, **kwargs) -> t_Any:
        """Request method, must return acceptable
        object as input for classification model."""
        raise NotImplementedError()

class YesNoQuestionnaire(_ClassificationDataInput):
    """
    >>> q = YesNoQuestionnaire()
    >>> q.get_prepared(True, False, True)
    (1, 0, 1)
    """
    def get_prepared(self, *user_answers: bool, **kwargs) -> Tuple[int, ...]:
        prepared = tuple(map(int, user_answers))
        return prepared

class MovementTest(_ClassificationDataInput):
    """
    >>> BAD, AVERAGE, GOOD = range(3)
    >>> m = MovementTest()
    >>> m.get_prepared(BAD, GOOD, AVERAGE)
    (0, 2, 1)
    """
    def get_prepared(self, *test_result_enums: int, **kwargs) -> Tuple[int, ...]:
        prepared = test_result_enums
        return prepared
```

**Java**

```java
public abstract class Developer {
}

// Так делать плохо:
public class Worker extends Developer {
    public int skill; // -1 junior, 0 middle, 1 senior

    public Worker(int skill){
        this.skill = skill;
    }
}


// Лучше делать так:
public class Senior extends Developer {
}

public class Middle extends Developer {
}

public class Junior extends Developer {
}

// Теперь наш код открыт для расширений, но закрыт для изменений, 
// и с точки зрения семантики так куда лучше :)
```

Проанализировав эталонное решение, понял, что показал все верно.