from typing import TypeVar, Self, Union
from copy import deepcopy
import pickle
from itertools import starmap
import operator

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

class Vector(Any):
    def __init__(self, *args : Any, **kwargs):
        super().__init__(*args, **kwargs)
        self._size = len(args)
        self.array = args
    
    # приципиально добавить переопрдееление этого метода, для дальнейшего вложенного сложения
    # без него будет вызов sum() у NoneType
    def __add__(self, other: Self) -> Union[Self, Null]:
        try:
            assert self._size == other._size
        except AssertionError:
            sum_vector = Null
        else:
            sum_vector = self.sum(other)

        return sum_vector

    def sum(self, v : Self) -> Self:
        items = starmap(operator.add, zip(self.array, v.array))
        result_vector = Vector(*items)

        return result_vector
    
    
v1 = Vector(1, 2, 3)
v2 = Vector(1, 2, 3)

v_result = v1 + v2
print(v_result.array) # [2, 4, 6]

v1 = Vector("1", "2", "3")
v2 = Vector("1", "2", "3")

v_result = v1 + v2
print(v_result.array) # ['11', '22', '33']

v1 = Vector((
        Vector(1, 1),
        Vector(2, 2)
    )
)

v2 = Vector((
        Vector(5, 5),
        Vector(10, 10)
    )
)

v_result = v1 + v2
print(v_result.array)
# [[[6, 6], [12, 12]]]


v1 = Vector("1", "2", "3")
v2 = Vector("1", "2")

v_result = v1 + v2
print(v_result is Null) # Different size

