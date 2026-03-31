from typing import TypeVar
from copy import deepcopy
import pickle

T = TypeVar('T', covariant=True)
S = TypeVar('S', covariant=True)

# закрытый для изменений
class General(object):
    COPY_NIL = 0
    COPY_OK = 1
    COPY_ATTR_ERR = 0

    ASSIGMENT_NIL = 0
    ASSIGMENT_OK = 1
    ASSIGMENT_MISS = 2

    def __get_status_fields(self) -> set:
        fields = set(attr for attr in dir(self)
                     if attr.endswith('status'))
        return fields
    
    def __init__(self, *args, **kwargs):
        self._copy_status = self.COPY_NIL
        self._assignment_status = self.ASSIGMENT_NIL
        self._value = Null()

    def __get_status_fields(self) -> set:
        fields = set(attr for attr in dir(self)
                     if attr.endswith('status'))
        return fields
    
    # обход всех аттрибутов внутри объекта и копирование их в текущий
    
    def copy(self, obj_from : T):
        if not (type(self) is type(obj_from)):
            self._copy_status = self.COPY_ATTR_ERR
            return
        
        status_fields = self.__get_status_fields()
        attributes = filter(lambda a: a not in status_fields,
                            dir(self))
        
        if not all(hasattr(obj_from, attr) for attr in attributes):
            self._copy_status = self.COPY_ATTR_ERR
            return
        
        for attr in attributes:
            target = getattr(obj_from, attr)
            setattr(self, attr, deepcopy(target))
        
        self._copy_status = self.COPY_OK
    
    # возвращает результат copy
    
    def clone(self, obj_from : T) -> T:
        new_obj = self.__class__.__new__(self.__class__)
        new_obj.copy(obj_from)

        if new_obj._copy_status != self.COPY_OK:
            return
        
        return new_obj
    
    def __eq__(self, target) -> bool:
        return self.__dict__ == target.__dict__

    # перевод аттрибутов в строку json
    
    def serialize(self) -> bytes:
        return pickle.dumps(vars(self))

    # перевод из строки в аттрибуты текущего объекта
    
    def deserialize(self, target : bytes) -> T:
        return pickle.loads(target)

    # вывод всех аттрибутов (лучше переопределить __str__, чем использовать print)
    
    def __str__(self):
        print(
            str(vars(self))
        )

    
    def check_type(self, target_type : T) -> bool:
        return type(self) is target_type

    
    def type(self) -> T:
        return self.__class__
    
    @classmethod
    def assignment_attempt(cls, target : T, source : S):
        if isinstance(source, type(target)):
            target._value = source._value
            target._assignment_status = cls.ASSIGMENT_OK
            return
        
        target._value = Null()
        target._assignment_status = cls.ASSIGMENT_MISS
    
    def get_assignment_attempt_status(self) -> int:
        return self._assignment_status
    
    def get_base_value(self):
        return self._value

# открытый для изменений
class Any(General):
    pass

class Null(General):
    def __new__(self, *args, **kwargs):
        return None # переопределяем и делаем его закрытым и пустым, таким образом у нас при вызове методов будет возникать ошибка

class Vehicle(Any):
    def __init__(self, type: str):
        super().__init__()
        self.type = type

class Bysicle(Vehicle):
    def __init__(self, type):
        super().__init__(type)

    def drive(self):
        print("drive!!!")

class ElectricBysicle(Bysicle):
    def __init__(self, type):
        super().__init__(type)

    def drive(self):
        print("drive wit electricity engine!!!")

# тест
bike1 = Bysicle(type="велик")
bike2 = ElectricBysicle(type="электровелик")

# ElectricBysicle потомок Bysicle — успех
Bysicle.assignment_attempt(bike1, bike2)
print(bike1.get_assignment_attempt_status())  # 1 — ASSIGNMENT_OK
print(bike1.get_base_value())              # ElectricBysicle объект

# Bysicle не потомок ElectricBysicle — неудача
Bysicle.assignment_attempt(bike2, bike1)
print(bike2.get_assignment_attempt_status())  # 2 — ASSIGNMENT_MISS
print(bool(bike2.get_base_value()))        # False — Null