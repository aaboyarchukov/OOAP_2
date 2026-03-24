# Принцип Открыт/Закрыт применительно к иерархии классов

### OCP
---

На прошлом занятии мы говорили о OCP, в разрезе [[Общая структура иерархии классов в проекте|иерархии классов]], так как по сути мы ограничили возможность модификации класса `General` и  предоставили для изменений его наследника `Any`.

В некоторых случаях, когда нет возможности запрета на переопределения методов, используют пары методов, один закрытый - базовый, другой открытый для переопределения, таким образом мы сохраняем семантику и соблюдаем OCP, но накладываем дополнительные нагрузки на написание двух методов.

### Примеры в разных ЯП
---

#### Go
В данном ЯП нельзя явно указать запрет на переопределение методов, в принципе в нем не переопределить методы, а только имплементировать, ведь как такового механизма наследования у Go - нет.

#### Python
Декоратор позволяет 'зафиксировать' метод и запрещает его переопределять.

Пример:

```python
def final(method):
    method.__final__ = True
    return method

class Meta(type):
    def __new__(mcs, name, bases, namespace):
        for base in bases:
            for attr, value in namespace.items():
                base_method = getattr(base, attr, None)
                if base_method and getattr(base_method, '__final__', False):
                    raise TypeError(
                        f"Метод '{attr}' в классе '{base.__name__}' "
                        f"запрещён для переопределения"
                    )
        return super().__new__(mcs, name, bases, namespace)

class Animal(metaclass=Meta):
    @final
    def eat(self):
        print("ест")

    def sound(self):  # этот можно переопределять
        print("звук")

class Cat(Animal):
    def sound(self):   # OK
        print("мяу")

    def eat(self):     # ОШИБКА при создании класса
        print("ест по-кошачьи")
```

#### Java
В Java есть ключевое слово `final` в семантике метода, для запрета на переопределение:

```java
class Animal {
    public final void eat() {    // final — нельзя переопределить
        System.out.println("ест");
    }

    public void sound() {        // можно переопределять
        System.out.println("звук");
    }
}

class Cat extends Animal {
    @Override
    public void sound() {        // OK
        System.out.println("мяу");
    }

    @Override
    public void eat() {          // ОШИБКА компиляции
        System.out.println("ест по-кошачьи");
    }
}
```
