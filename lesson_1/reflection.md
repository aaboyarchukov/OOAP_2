# Наследование, композиция и полиморфизм

В данном уроке мы изучим такие механизмы в ООП как:

- наследование
- полиморфизм
- композиция

---

1. Наследование - механизм, который позволяет переиспользовать существующий код, работает на основе выстроения иерархии классов, когда у нас есть родители и их дети, дети имеют все доступные свойства родителей и могут их переопределять, также внедряя свои, или ограничивая родительские. Следует использовать наследование при организации оотношения `is-a` между классами

В Go нет насоедования как такового, существует только встраивание и полиморфизм за счет имплементации интерфейсов. Поэтому именно наследование проще показать на другом ЯП, например (python, java):

### Пример:

***Транспорт***

В данном примере мы показали наследование транспорта, где наследником является машина, то есть можно сказать, что у нас сохраняется отношение
##### `Car is-a Vehicle`

```python
class Vehicle():
	__type_name = "Транспорт"
	
	@classmethod
	def get_type(cls):
		return cls.__type_name
	
	def move(cls):
		print(f'Едет {cls.__type_name}')
	
	def __init__(self, max_speed):
		self.max_speed = max_speed
	
	def info(self):
		print(f'Максимальная скорость {self.max_speed}')
	
	

class Car(Vehicle):
	__type_name = "Машина"
	
	def __init__(self, wheels, doors, weight_kg, max_speed):
		super().__init__(max_speed)
		self.wheels = wheels
		self.doors = doors
		self.weight_kg = weight_kg
	
	def info(self):
		super().info()
		
		print(f'Количество дверей {self.doors}')
		print(f'Количество колес {self.wheels}')
		print(f'Масса {self.weight_kg}')
	
```

***Геометрические фигуры***

В данном примере мы показали наследование фигур, где окружность является наследником эллипса, то есть можно сказать, что у нас сохраняется отношение
##### `Circle is-a Ellipse`

Также есть неебольшая композиция, в виде встраивания класса (записи) `Point`

```java
public interface Shape {
	double area();
	double perimeter();
}

public record Point(double x, double y) {
	// ...
}

public class Ellipse implements Shape {
	private Point f1; // composition
	private Point f2; // composition
	
	@Override
	public double area() {
		//...
	}
	
	@Override
	public double perimeter() {
		//...
	}
}

public class Circle extends Ellipse {
	private Point center;
    private double radius;
	
	@Override
	public double area() {
		//...
	}
	
	@Override
	public double perimeter() {
		//...
	}
}
```

---

2. Полиморфизм - механизм, при котором тип может менять свою "форму" - становится объектами разных типов

### Пример:

Здесь мы вызываем функцию, в которую передаем дочерний тип `Vehicle`, код скомпилируется и верно исполнится, так как наш класс `Car` является дочерним по отношению к `Vehicle`

При росте иерархии классов мы сможем передавать совершенно другие типы и на основе динамического полиморфизма, у нас все будет исполнятся все верно!

```python
def get_vehicle_info(vehicle : Vehicle):
	vehicle.info()

get_vehicle_info(Car(4, 4, 300, 150))
```

То же самое на фигурах, где мы передаем дочерний класс. Также мы можем сделать другую функцию, где будет полиморфизм через интерфейс `Shape`, что тоже будет корректно

```java
public double GetArea(ellipse Ellipse) {
	return ellipse.area();
}

// или

public double GetArea(shape Shape) {
	return shape.area();
}

GetArea(new Circle(...))
GetArea(new Ellipse(...))
```

В Go это делается также через интерфейс:

Делаем на примере попугая!

```go
type Parrot interface {
	Speed() float32
	Weight() float32
	Сolor() string
}

type AfricanParrot struct {
	Speed float64
	Weight float64
	Color string
}

func (afp *AfricanParrot) Speed() float32 {}
func (afp *AfricanParrot) Weight() float32 {}
func (afp *AfricanParrot) Сolor() float32 {}

type EuropianParrot struct {
	Speed float64
	Weight float64
	Color string
}

func (ep *EuropianParrot) Speed() float32 {}
func (ep *EuropianParrot) Weight() float32 {}
func (ep *EuropianParrot) Сolor() float32 {}

func GetParrotInfo(parrot Parrot) {
	// invoke methods
}

GetParrotInfo(EuropianParrot{...})
GetParrotInfo(AfricanParrot{...})

```

---

3. Композиция - механизм при котором в класс встривается объект другого класса, тем самым не наследуются, но у текущего класса появляется доступ к методам встроенного класса! Здесь в отличие от наследование реализуется отношение `has-a`

### Пример:

Здесь у машины появился двигатель, мы в методе инициализации передали атрибут типа `Engine`, тем самым у машины есть доступ к двигателю и сохраняется отношение

##### `Car has-a Engine`

```python
class Vehicle():
	__type_name = "Транспорт"
	
	@classmethod
	def get_type(cls):
		return cls.__type_name
	
	def move(cls):
		print(f'Едет {cls.__type_name}')
	
	def __init__(self, max_speed):
		self.max_speed = max_speed
	
	def info(self):
		print(f'Максимальная скорость {self.max_speed}')
	

class Engine():
	def __init__(self, power):
		self.power = power

class Car(Vehicle):
	__type_name = "Машина"
	
	def __init__(self, wheels : int, doors : int, weight_kg : float, max_speed : int, engine : Engine:
		super().__init__(max_speed)
		self.wheels = wheels
		self.doors = doors
		self.weight_kg = weight_kg
		self.engine = engine
	
	def info(self):
		super().info()
		
		print(f'Количество дверей {self.doors}')
		print(f'Количество колес {self.wheels}')
		print(f'Масса {self.weight_kg}')
		print(f'Мощность {self.engine.power}')
	
```

Но много кто предпочитает композицию наследованию по нескольким причинам:
1. необходимость переопределять методы. 
2. жесткая связь, при изменении родителя, необходимо менять детей
3. тестирование, дочерний класс тянет за собой родительский