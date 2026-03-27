from typing import TypeVar
from copy import deepcopy
import pickle

T = TypeVar('T', covariant=True)

# закрытый для изменений
class General(object):
    COPY_NIL = 0
    COPY_OK = 1
    COPY_ATTR_ERR = 0

    def __get_status_fields(self) -> set:
        fields = set(attr for attr in dir(self)
                     if attr.endswith('status'))
        return fields
    
    def __init__(self, *args, **kwargs):
        self.copy_status = self.COPY_NIL

    def __get_status_fields(self) -> set:
        fields = set(attr for attr in dir(self)
                     if attr.endswith('status'))
        return fields
    
    # обход всех аттрибутов внутри объекта и копирование их в текущий
    @final
    def copy(self, obj_from : T):
        if not (type(self) is type(obj_from)):
            self.copy_status = self.COPY_ATTR_ERR
            return
        
        status_fields = self.__get_status_fields()
        attributes = filter(lambda a: a not in status_fields,
                            dir(self))
        
        if not all(hasattr(obj_from, attr) for attr in attributes):
            self.copy_status = self.COPY_ATTR_ERR
            return
        
        for attr in attributes:
            target = getattr(obj_from, attr)
            setattr(self, attr, deepcopy(target))
        
        self.copy_status = self.COPY_OK
    
    # возвращает результат copy
    @final
    def clone(self, obj_from : T) -> T:
        if self.copy_status != self.COPY_OK:
            return
        
        return self.copy(obj_from)
    @final
    def __eq__(self, target) -> bool:
        return self.__dict__ == target.__dict__

    # перевод аттрибутов в строку json
    @final
    def serialize(self) -> bytes:
        return pickle.dumps(vars(self))

    # перевод из строки в аттрибуты текущего объекта
    @final
    def deserialize(self, target : bytes) -> T:
        return pickle.loads(target)

    # вывод всех аттрибутов (лучше переопределить __str__, чем использовать print)
    @final
    def __str__(self):
        print(
            str(vars(self))
        )

    @final
    def check_type(self, target_type : T) -> bool:
        return type(self) is target_type

    @final
    def type(self) -> T:
        return self.__class__

# открытый для изменений
class Any(General):
    pass

class Vehicle(Any):
    def __init__(self, type: str):
        self.type = type

class Bysicle(Vehicle):
    def drive():
        print("drive!!!")

class ElectricBysicle(Any, Bysicle):
    def drive():
        print("drive wit electricity engine!!!")

class Null(ElectricBysicle):
    def __new__(self, *args, **kwargs):
        return None # переопределяем и делаем его закрытым и пустым, таким образом у нас при вызове методов будет возникать ошибка