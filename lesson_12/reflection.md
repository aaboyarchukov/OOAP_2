# Попытка присваивания

### Присваивание 
---
При использовании полиморфных объектов возникает ошибка, которая свидетельствует о неправильной архитектуре:

```
if type(object) is LinkedList then ...
else if type(object) is TwoWayList then ...
```

появляются проверки такого типа, а это плохо!

Этому свидетельствует две причины:

1. Рост цикломатической сложности в проекте
2. Архитектурно, в ООП не принято писать такие проверки, все делается на уровне тайп-чекинга, компилятором. Избавляются от такого путем **замены операции присваивания на более безопасную версию**. Если код прошёл тайп-чекинг — никаких дополнительных проверок типа быть не должно.

Можно прибегнуть к следующему методу:

```python
def assignment_attempt(target : T, source : S)
```

мы будем писать команду по присваиванию определенного типа, и у нас либо будет успех, либо будет присвоен `target` Null-object, который оставит нас в рамках системы типов.
И важно, что мы не получаем ошибку или исключение, у нас просто идет несоответствие типов, таким образом наша система остается стабильной.

Особенно полезно это при обработке случая, когда тип заранее неизвестен и нам требуется проверка.

### Решение
---
[example.py](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_12/example.py)

```python
# ...
def assignment_attempt(self, source : S):
        if isinstance(source, type(self)):
            self._value = deepcopy(source)
            self._assignment_status = self.ASSIGMENT_OK
            return
        
        self._value = Null()
        self._assignment_status = self.ASSIGMENT_MISS
# ...
```


### Рефлексия
---
Эталонное решение:

Python


```python
class Any(General):
	@classmethod
	def assignment_attempt(cls, target, source):
		if isinstance(target, cls) and isinstance(source, cls):
			target.value = source.value
			return target
		return Void
```

Java

```java
class General implements Serializable {

    public static <TFrom extends Any, TTo extends Any>
            TTo assignmentAttempt(TFrom from, TTo to) {

        var classFrom = from.getType();
        var classTo = to.getType();
        if (classTo.isAssignableFrom(classFrom)) {
            return (TTo) from;
        }
        return None;
    }
```

Проанализировав эталонное решение, понял, допустил некоторые ошибки:
- метод является не статическим
- нет симметричного сравнения
- метод является командой и ничего не возвращает (оставлю таким же)

Решение после рефлексии:

[example.py](https://github.com/aaboyarchukov/OOAP_2/blob/main/lesson_12/example.py)

```python
 @classmethod
    def assignment_attempt(cls, target : T, source : S):
        if isinstance(source, type(target)):
            target._value = source._value
            target._assignment_status = cls.ASSIGMENT_OK
            return
        
        target._value = Null()
        target._assignment_status = cls.ASSIGMENT_MISS
```