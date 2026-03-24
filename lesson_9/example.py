from typing import TypeVar
from copy import deepcopy
import json

T = TypeVar('T', covariant=True)

# закрытый для изменений
class General(object):

    # обход всех аттрибутов внутри объекта и копирование их в текущий
    def copy(self, obj_from : T):
        if not (type(self) is type(obj_from)):
            return
        
        attributes = vars(obj_from)
        for attr in attributes:
            target = getattr(obj_from, attr)
            setattr(self, attr, deepcopy(target))
    
    # возвращает результат copy
    def clone(self, obj_from : T) -> T:
        return self.copy(obj_from)

    def __eq__(self, target) -> bool:
        if type(self) is type(target):
            return False
        
        target_attributes = vars(target)
         
        for attr in target_attributes:
            
            target_val = getattr(target, attr)
            self_val = getattr(self, attr)
            
            # сравнение будет корректно, так как
            # я переопределяю именно метод __eq__,
            # а значит он будет автоматически переопределен для потомков
            if target_val != self_val:
                return False
            
        return True

    # перевод аттрибутов в строку json
    def serialize(self):
        return json.dumps(vars(self))

    # перевод из строки в аттрибуты текущего объекта
    def deserialize(self, target_row : str):
        target_dict : dict = json.loads(target_row)
        for attr, value in target_dict.items():
            setattr(self, attr, value)

    # вывод всех аттрибутов (лучше переопределить __str__, чем использовать print)
    def __str__(self):
        print(
            str(vars(self))
        )

    def check_type(self, target_type : T) -> bool:
        return type(self) is target_type

    def type(self) -> T:
        return self.__class__

# открытый для изменений
class Any(General):
    pass