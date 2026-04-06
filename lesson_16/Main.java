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