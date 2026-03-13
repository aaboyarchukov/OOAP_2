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
	
	def __init__(self, wheels : int, doors : int, weight_kg : float, max_speed : int, engine : Engine):
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
	