# Полиморфность и ковариатность

### Полиморфность и ковариантность
---
Использование двух подходов в рамках вызова методов или инициализации объекта, может привести к непредвиденным результатам, о чем мы писали раннее [[Пример динамического связывания и полиморфизма#Ковариантность и контравариантность|тут про ковариантность]] и [[Наследование, композиция и полиморфизм 1#^1057a6|тут про полиморфизм]] , а именно непредвиденный результат возникнет, когда мы полиморфно назначим другой объект текущему и попытаемся ковариантно вызвать метод от него.

Наша задача сделать строже систему и не допустить появление в программе использования как полиморфизма, так и ковариантности одновременно.

### Примеры
---

В Python ковариатность доступна каждому объекту без ограничений, поэтому его пример не показательный

```python
class Animal:
    def __init__(self, animal_type):
        self.animal_type = animal_type
    
    def sound(self):
        print("sound")

class Dog(Animal):
    def __init__(self, animal_type):
        super().__init__(animal_type)
    
    def sound(self):
        print("gav")

class Cat(Animal):
    def __init__(self, animal_type):
        super().__init__(animal_type)
    
    def sound(self):
        print("miau")

# polimorphism
def sound_animal(a : Animal):
    a.sound()

sound_animal(Animal("animal"))
sound_animal(Dog("dog"))
sound_animal(Cat("cat"))

# covariaty
def sound_sequence_of_animals(list_of_animals : list[Animal]):
    for animal in list_of_animals:
        animal.sound()
```

Но вот в Java изначально все объекты инваринтны, но можно сделать их ковариантными с помощью ключевого слова `extends`:

```java
package lesson_16;

import java.util.List;

public class Main {
    public void main() {

    }

    // polimorphism
    public void SoundAnimal(Animal animal) {
        animal.sound();
    }

    // covariaty
    public void SoundAnimals(List<? extends Animal> animals) {
        animals.add(new Dog()); // apply covariaty with extends
        for (Animal animal : animals) {
            animal.sound();
        }
    }
}
```

### Рефлексия
---
Эталонные решения:

**Python**

```python
# Полиморфный вызов.

class Person():
    def walk(self):
        print('Yes, i can walk...')

# Наследник расширяет класса-предок
# новым методом:
class Baker(Person):
    def bake(self):
        print('and bake!')

somebody = Baker()

# Тип Baker ведет себя как тип Person
# при вызове этого метода:
somebody.walk()
```

```python
# Ковариантный вызов.

from typing import Generic, TypeVar, Callable

animal = TypeVar('animal', covariant=True)

class Animal():
    def make_sound(self):
        raise NotImplementedError

class Cat(Animal):
    def make_sound(self):
        print('Meow!')

class Dog(Animal):
    def make_sound(self):
        print('Woof!')

# ящик на вход принимает любой объект типа Animal
class Box(Generic[animal]):
    def __init__(self, content: animal) -> None:
        self._content = content

    def make_sound(self):
        self._content.make_sound()

# Ковариантный вызов:
def shake_box(box: Box[Animal]):
    box.make_sound()

some_animal = Cat()
box = Box(some_animal)
shake_box(box)
```

**Java**

```java
class Expression {
    @Override
    public String toString() {
        return "some expression";
    }

    public void method() {
        System.out.println("some method from expression");
    }
}

class SimpleExpression extends Expression {
    @Override
    public String toString() {
        return "some simple expression";
    }

    @Override
    public void method() {
        System.out.println("some method from simple expression");
    }
}

class ComplexExpression extends SimpleExpression {
    @Override
    public String toString() {
        return "some complex expression";
    }

    @Override
    public void method() {
        System.out.println("some complex expression");
    }
}


class Calculator {
    Expression getExpression() {
        System.out.println("Некоторая логика простого калькулятора");
        return new Expression();
    }

    // В Java только массивы ковариантны,
    // остальные обобщенные коллекции использовать нельзя.
    public <T extends Expression> void covariantMethod(T[] values) {
        for (T value : values) {
            System.out.println(value.toString());
        }
    }

    // Можно передавать как объект типа Expression, 
    // так и любого его потомка
    public void polymorphicMethod(Expression value) {
        value.method();
    }
}

class EngineeringCalculator extends Calculator {
    @Override
    SimpleExpression getExpression() {
        System.out.println("Некоторая логика инженерного калькулятора");
        return new SimpleExpression();
    }

    @Override
    public <T extends Expression> void covariantMethod(T[] values) {
        super.covariantMethod(values);
        System.out.println(values.length);
    }
}

...

Calculator calculator = new EngineeringCalculator();
Expression[] expressions = new Expression[2];
expressions[0] = new SimpleExpression();
expressions[1] = new ComplexExpression();

// пример вызовы ковариантного метода (только для массивов)
calculator.covariantMethod(expressions);

// пример вызова полиморфного метода 
// передаем наследника класса Expression, 
// а не объект класса Expression
calculator.polymorphicMethod(new SimpleExpression());
```

Проанализировав эталонное решение понял, что допустил некоторые неточности:
- в примере с Java забыл уточнить, что ковариантными по-умолчанию являются только массивы
```java
Animal[] animals = new Dog[3];
animals[0] = new Cat();
```
но стоит заметить, что ковариантными можно сделать и другие `iterable` дженерик типы с помощью `extends`