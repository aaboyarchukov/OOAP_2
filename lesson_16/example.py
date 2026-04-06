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