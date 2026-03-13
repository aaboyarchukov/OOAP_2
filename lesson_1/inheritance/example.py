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
	