# Полиморфность и ковариатность

### Полиморфность и ковариантность
---
Использование двух подходов в рамках вызова методов или инициализации объекта, может привести к непредвиденным результатам, о чем мы писали раннее [тут про ковариантность](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_8/reflection.md#:~:text=Ковариантность%20и%20контравариантность) и [тут про полиморфизм](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_1/reflection.md#:~:text=Полиморфизм%20%2D%20механизм%2C%20при%20котором%20тип%20может%20менять%20свою%20%22форму%22%20%2D%20становится%20объектами%20разных%20типов) , а именно непредвиденный результат возникнет, когда мы полиморфно назначим другой объект текущему и попытаемся ковариантно вызвать метод от него.

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