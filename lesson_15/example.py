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