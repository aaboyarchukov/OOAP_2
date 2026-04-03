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

### Рефлексия
---
Эталонное решение:

**Python**

```python
class Any(General):

    ... 

    def __add__(self, other):
        """Summation"""
        raise NotImplementedError()

class Vector(Any):
    """
    >>> v1 = Vector(0, 1, 2)
    >>> v2 = Vector(7, 10, 15)
    >>> (v1 + v2).get_sequence_representation()
    (7, 11, 17)
    >>> v3 = Vector(3)
    >>> (v1 + v3) is Void
    True
    >>> v4 = Vector(6)
    >>> nested_v1 = Vector(Vector(v1), Vector(v3))
    >>> nested_v2 = Vector(Vector(v2), Vector(v4))
    >>> nested_v1.get_sequence_representation()
    (((0, 1, 2),), ((3,),))
    >>> nested_v2.get_sequence_representation()
    (((7, 10, 15),), ((6,),))
    >>> (nested_v1 + nested_v2).get_sequence_representation()
    (((7, 11, 17),), ((9,),))
    """

    def __init__(self, *args: t_Any, **kwargs):
        super().__init__(*args, **kwargs)
        self.sequence = args
        self._size = len(args)

    def __add__(self, other: 'Vector') -> Union['Vector', Void]:
        try:
            assert self._size == other._size
        except AssertionError:
            sum_vector = Void
        else:
            sum_vector = self._sum_vectors(other)
        return sum_vector

    def _sum_vectors(self, other: 'Vector') -> 'Vector':
        sequence_items = starmap(operator.add, zip(self.sequence, other.sequence))
        sum_vector = Vector(*sequence_items)
        return sum_vector

    def get_sequence_representation(self) -> tuple:
        """Get representation of all nested sequence (recursive)"""
        this_func_name = self.get_sequence_representation.__name__
        representation = tuple(
                getattr(item, this_func_name, lambda: item)()
                for item in self.sequence)
return representation
```

**Java**

```java
public class Adder<T> extends Any {

    public T sum(T first, T second){

        T ans = null;

        if(first instanceof String){
            ans = sumString(first, second);
        }

        if(first instanceof Integer){
            ans = sumInteger(first, second);
        }

        if (first instanceof Double){
            ans = sumDouble(first, second);
        }

        return ans;
    }

    private T sumString(T first, T second){
        return (T)(first + (String)second);
    }

    private T sumInteger(T first, T second){
        Integer sum = (Integer)first + (Integer)second;
        T value = (T)sum;
        return value;
    }

    private T sumDouble(T first, T second){
        return (T)((Double)((Double)(first) + (Double)second));
    }
}

public class Vector<T> extends Adder {

    public static int ADD_NIL = 0;
    public static int ADD_OK = 1;
    public static int ADD_ERR = 2;

    private int length;
    private T[] arr;
    private int add_status;

    public Vector(T[] arr){
        this.arr = arr;
        length = arr.length;
        add_status = ADD_NIL;
    }

    public Vector(int length){
        arr = (T[])new Object[length];
        this.length = length;
        add_status = ADD_NIL;
    }

    public void add(Vector<? extends T> v){
        Vector<String> temp = new Vector<String>(1);
        if (v.getLength() == length){
            T[] arr2 = v.getArr();

            for (int i = 0; i < length; i++){
                if(arr2[i].getClass().isInstance(temp)){ 
                // проверяем типы. Если это Vector, то:
                    ((Vector<T>)arr[i]).add(((Vector<T>)arr2[i]));
                }
                else { // иначе - это Number или String
                    add_v((Vector<T>) v);
                    add_status = ADD_OK;
                    break;
                }
            }

            add_status = ADD_OK;
        }
        else{
            add_status = ADD_ERR;
        }
    }

    private void add_v(Vector<T> v){
        T[] arr2 = v.getArr();
        for(int i = 0; i < length; i++){
            arr[i] = (T) sum(arr[i], arr2[i]);
        }
    }

    public static Vector addVectors(Vector v1, Vector v2){
        Vector ans = (Vector)v1.deepCopy();

        ans.add(v2);

        return ans;
    }

    public int getLength(){
        return length;
    }

    public int get_add_status(){
        return add_status;
    }

    public T[] getArr(){
        return arr;
    }
}
```

Проанализировав эталонное решение понял, что допустил некоторые ошибки. Решение после рефлексии:

[example.py](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_14/example.py)

```python
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
```