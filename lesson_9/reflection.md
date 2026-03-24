# Общая структура иерархии классов в проекте

### Иерархия классов в проекте
---

При построении программы - наша задача состоит в том, чтобы организовать грамотную иеррахию классов - где в самом верху будет класс определяющий общие методы, не поддающиеся изменениям. От этого класса наследуются все объекты программы (неявно), например, как `object` в Java/C#.

Такой класс должен реализовывать базовые операции, такие как:

-- **копирование объекта** (копирование содержимого одного объекта в другой существующий, включая DeepCopy -- глубокое рекурсивное дублирование, подразумевающее также копирование содержимого объектов, вложенных в копируемый объект через его поля, атрибуты);   
-- **клонирование объекта** (создание нового объекта и глубокое копирование в него исходного объекта);  
-- **сравнение объектов** (включая глубокий вариант);  
-- **сериализация/десериализация** (перевод в формат, подходящий для удобного ввода-вывода, как правило в строковый тип, и восстановление из него);  
-- **печать** (наглядное представление содержимого объекта в текстовом формате);  
-- **проверка типа** (является ли тип текущего объекта указанным типом);   
-- **получение реального типа объекта** (непосредственного класса, экземпляром которого он был создан).

Ну при добавлении нового класса, мы наследуем его от самого верхнего в иерархии, но не того, который недоступен к изменениям, а тот кто открыт. То есть:

```python
# мы обозначаем клас General, который закрыт к изменениям
# и определяет основные операции

# закрытый для изменений
class General(object):
	pass
	
# но от него наследуем другой класс, который будет открыт для изменений

# открытый для изменений
class Any(General):
    pass
    
# и вот уже новые классы будут унаследованы от Any
```

Вот как должны выглядеть классы:

```python
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
```

### Рефлексия
---

Эталонное решение:

```python
_T = TypeVar('_T')


class General(object):

    COPY_NIL = 0       # copy_to() not called yet
    COPY_OK = 1        # last copy_to() call completed successfully
    COPY_ATTR_ERR = 2  # other object have no attribute copied from this object

    def __get_status_fields(self) -> set:
        fields = set(attr for attr in dir(self)
                     if attr.endswith('status'))
        return fields

    def __init__(self, *args, **kwargs):
        self._copy_status = self.COPY_NIL

    # commands:
    @final
    def copy_to(self, other: _T) -> None:
        """Deep-copy of attributes of **self** to **other** with
        ignoring status-attributes."""
        status_fields = self.__get_status_fields()
        copy_attrs = filter(lambda a: a not in status_fields,
                            dir(self))

        if not all((hasattr(other, a) for a in copy_attrs)):
            self._copy_status = self.COPY_ATTR_ERR
            return

        for attr in copy_attrs:
            value = deepcopy(getattr(self, attr))
            setattr(other, attr, value)

        self._copy_status = self.COPY_OK

    # requests:
    @final
    def __eq__(self, other: _T) -> bool:
        return self.__dict__ == other.__dict__

    @final
    def __repr__(self) -> str:
        s = f'<"{self.__class__.__name__}" instance' \
            f' (id={id(self)})>'
        return s

    @final
    def clone(self) -> _T:
        clone = deepcopy(self)
        return clone

    @final
    def serialize(self) -> bytes:
        bs = pickle.dumps(self)
        return bs
    @final
    @classmethod
    def deserialize(cls, bs: bytes) -> _T:
        instance = pickle.loads(bs)
        return instance

    # method statuses requests:
    @final
    def get_copy_status(self) -> int:
        """Return status of last copy_to() call:
        one of the COPY_* constants."""
        return self._copy_status


class Any(General):
    """
    >>> a = Any()
    >>> isinstance(a, Any), isinstance(a, General)
    (True, True)
    >>> type(a) == Any, type(a) == General
    (True, False)
    >>> b = Any()
    >>> a.copy_to(b)
    >>> a.get_copy_status() == a.COPY_OK
    True
    >>> a == b, a is b  # different because of _copy_status
    (False, False)
    >>> bs = a.serialize()
    >>> deser_a = Any.deserialize(bs)
    >>> a == deser_a, a is deser_a
    (True, False)
    >>> a_clone = a.clone()
    >>> a == a_clone, a is a_clone
    (True, False)
    >>> class A(Any):
    ...     def __init__(self, nested_dict: dict, **kwargs):
    ...         super().__init__(nested_dict, **kwargs)
    ...         self.d = nested_dict
    >>> nested1 = A({'d': {(4,56,3): {'f': 518, 'sdd9': {45: None}}}})
    >>> nested2 = A({'d': {(4,56,3): {'f': 518, 'sdd9': {45: None}}}})
    >>> nested1 == nested2
    True
    >>> nested3 = A({'d': {(4,56,3): {'f': 518, 'sdd9': {45: ''}}}})
    >>> nested1 == nested3
    False
    """
```

```java
class General implements Serializable {
    public <T> void deepCopy(T target) throws Exception {
        try {
            target = getCopy();
        } catch (Exception e) {
            throw e;
        }
    }

    public <T> T deepClone() throws Exception {
        try {
            return getCopy();
        } catch (Exception e) {
            throw e;
        }
    }

    @Override
    public boolean equals(Object obj) {
        return super.equals(obj);
    }

    public <T> String serialize() throws JsonProcessingException {
        var mapper = new ObjectMapper();
        return mapper.writeValueAsString((T)this);
    }

    public static <T> T deserialize(
                        String json, 
                        Class<T> clazz) throws JsonProcessingException {
        var mapper = new ObjectMapper();
        return mapper.readValue(json, clazz);
    }

    @Override
    public String toString() {
        return super.toString();
    }

    @JsonIgnore
    public final Class<?> getType() {
        return this.getClass();
    }

    private <T> T getCopy() throws Exception  {
        try {
            var byteArrayOutputStream = new ByteArrayOutputStream();
            var objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
            objectOutputStream.writeObject((T)this);
            var bais = new ByteArrayInputStream(byteArrayOutputStream.toByteArray());
            var objectInputStream = new ObjectInputStream(bais);

            return (T) objectInputStream.readObject();
        }
        catch (Exception e) {
            throw e;
        }
    }
}

/*public*/ class Any extends General {

}
```

Проанализиировав эталонное, понял, что допустил некоторые недочеты:
- для команд не написал запросы состояний (соответственно и фильтрация определенных аттрибутов класса)
- не проставил теги, которые определяют неизменяемость
- нет переменного количества аргументов в конструкторе
- более простая реализация сравнения

В остальном решение корректное. Вот решение после рефлексии:

```python
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
```