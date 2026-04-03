# Наследование, полиморфизм и обобщённые типы

В данном уроке мы разберемся с проблемой обобщенных типов - универсальностью

### Проблема универсальности
---
Проблема заключается в том, что при использовании обычных обобщенных типов - мы выходим за рамки нашей системы типов, а также статический анализатор в виде компилятора не видит какой именно тип придет, из-за этого отсутствует какая-либо доступность методов и предсказуемость.

### Ограниченная универсальность
---
Данную проблему можно решить тем, что определить в рамках нашей системы типов свой обобщеный, который будет реализовывать тот набор методов, который нам нужен.

### Пример
---
[example.py](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_14/example.py)

```python
class Variant(Any):
    @classmethod
    def sum(cls, g1 : Any, g2 : Any) -> Self:
        return g1 + g2

class Vector[T : Variant](General):
    def __init__(self, array : list[T], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.array = array
    
    # приципиально добавить переопрдееление этого метода, для дальнейшего вложенного сложения
    # без него будет вызов sum() у NoneType
    def __add__(self, other: Self) -> Self:
        return self.sum(other)
    
    def append(self, element : Variant):
        self.array.append(element)

    def sum(self, v : Self) -> Self:
        if len(self.array) != len(v.array):
            return Null()
        
        accum_array = []
        result_vector = Vector(accum_array)

        for indx, value in enumerate(v.array):
            target_result = Variant.sum(value, self.array[indx])
            result_vector.append(target_result)

        return result_vector
    
    def to_list(self) -> list:
        result = []
        for item in self.array:
            # Если элемент внутри тоже вектор — распаковываем его
            if isinstance(item, Vector):
                result.append(item.to_list())
            else:
                # Если это уже просто число/строка — добавляем как есть
                result.append(item)
        return result
```